import formidable from 'formidable'; 
import fs from 'fs';
import path from 'path';
import { exec } from 'child_process';

export const config = {
  api: {
    bodyParser: false,
  },
};

export default function handler(req, res) {
  const form = formidable({
    uploadDir: path.join(process.cwd(), 'public', 'uploads'),
    keepExtensions: true,
    maxFileSize: 20 * 1024 * 1024,
  });

  form.parse(req, (err, fields, files) => {
    if (err) {
      console.error('Erro ao processar upload:', err);
      return res.status(500).json({ message: 'Erro ao processar o upload', error: err });
    }

    const { industria, distribuidor } = fields;
    if (!industria || !distribuidor) {
      return res.status(400).json({ message: 'Campos de indústria e distribuidor são obrigatórios' });
    }

    if (!files.baseFuncional || !files.baseDistribuidor || !files.pfMargem) {
      return res.status(400).json({ message: 'Arquivos baseFuncional, baseDistribuidor e pfMargem são obrigatórios' });
    }

    const arquivoFuncional = files.baseFuncional[0].filepath;
    const arquivoDistribuidor = files.baseDistribuidor[0].filepath;
    const arquivoPfMargem = files.pfMargem[0].filepath;

    const scriptName = `conciliacao_${industria}_${distribuidor}.py`;
    const scriptPath = path.join(process.cwd(), 'scripts', scriptName);

    if (!fs.existsSync(scriptPath)) {
      return res.status(404).json({ message: `Script não encontrado: ${scriptName}` });
    }

    const outputFileTemp = path.join(process.cwd(), 'Conciliacao_Finalizada_Santa_Cruz.xlsx');
    const outputDir = path.join(process.cwd(), 'public', 'uploads', 'resultados');
    const outputFileFinal = path.join(outputDir, 'resultado_conciliacao.xlsx');

    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    exec(`python ${scriptPath} ${arquivoFuncional} ${arquivoDistribuidor} ${arquivoPfMargem} ${outputFileTemp}`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Erro ao executar o script: ${stderr}\nLog do script: ${stdout}`);
        return res.status(500).json({ message: 'Erro ao executar o script', error: stderr });
      }

      console.log(`Resultado do script: ${stdout}`);

      // Verifica se o arquivo foi gerado e move para o caminho esperado
      if (fs.existsSync(outputFileTemp)) {
        try {
          fs.renameSync(outputFileTemp, outputFileFinal);
          console.log('Arquivo movido para:', outputFileFinal);

          // Enviar a URL de download
          const downloadUrl = '/uploads/resultados/resultado_conciliacao.xlsx';
          res.status(200).json({ message: 'Script executado com sucesso', downloadUrl });
        } catch (renameError) {
          console.error('Erro ao mover arquivo:', renameError);
          res.status(500).json({ message: 'Erro ao processar o arquivo final', error: renameError });
        }
      } else {
        res.status(500).json({ message: 'Arquivo de saída não encontrado' });
      }
    });
  });
}
