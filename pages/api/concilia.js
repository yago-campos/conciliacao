import formidable from 'formidable';
import fs from 'fs';
import path from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';

const fsExists = promisify(fs.exists);
const fsRename = promisify(fs.rename);

export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(req, res) {
  const form = formidable({
    uploadDir: path.join(process.cwd(), 'public', 'uploads'),
    keepExtensions: true,
    maxFileSize: 150 * 1024 * 1024,
  });

  form.parse(req, async (err, fields, files) => {
    if (err) {
      console.error('Erro ao processar upload:', err);
      return res.status(500).json({ message: 'Erro ao processar o upload', error: err });
    }

    const { industria, distribuidor } = fields;
    if (!industria || !distribuidor) {
      return res.status(400).json({ message: 'Campos de indústria e distribuidor são obrigatórios' });
    }

    // Verificação específica para msd e GSC
    if (!files.baseFuncional || !files.baseDistribuidor || 
        (!files.pfMargem && (industria === 'msd' && distribuidor === 'gsc'))) {
      return res.status(400).json({ message: 'Arquivos obrigatórios estão faltando. O arquivo "pfMargem" é necessário'});
    }

    const arquivoFuncional = files.baseFuncional[0].filepath;
    const arquivoDistribuidor = files.baseDistribuidor[0].filepath;
    const arquivoPfMargem = files.pfMargem ? files.pfMargem[0].filepath : null;

    const scriptName = `conciliacao_${industria}_${distribuidor}.py`;
    const scriptPath = path.join(process.cwd(), 'scripts', scriptName);

    if (!await fsExists(scriptPath)) {
      return res.status(404).json({ message: `Script não encontrado: ${scriptName}` });
    }

    const outputFileTemp = path.join(process.cwd(), 'Conciliacao_Finalizada_Santa_Cruz.xlsx');
    const outputDir = path.join(process.cwd(), 'public', 'uploads', 'resultados');
    const outputFileFinal = path.join(outputDir, 'resultado_conciliacao.xlsx');

    if (!await fsExists(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    try {
      exec(`python ${scriptPath} ${arquivoFuncional} ${arquivoDistribuidor} ${arquivoPfMargem ? arquivoPfMargem : ''} ${outputFileTemp}`, async (error, stdout, stderr) => {
        if (error) {
          console.error(`Erro ao executar o script: ${stderr}\nLog do script: ${stdout}`);
          return res.status(500).json({ message: 'Erro ao executar o script', error: stderr });
        }

        console.log(`Resultado do script: ${stdout}`);

        if (await fsExists(outputFileTemp)) {
          try {
            await fsRename(outputFileTemp, outputFileFinal);
            console.log('Arquivo movido para:', outputFileFinal);

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
    } catch (executionError) {
      console.error('Erro inesperado:', executionError);
      res.status(500).json({ message: 'Erro inesperado durante a execução do script', error: executionError });
    }
  });
}
