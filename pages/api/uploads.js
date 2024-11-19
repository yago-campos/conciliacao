import path from 'path';
import fs from 'fs';

export default function handler(req, res) {
  const { path: filePath } = req.query;

  // Caminho completo do arquivo na pasta /uploads
  const fullPath = path.join(process.cwd(), 'uploads', filePath);

  // Verifica se o arquivo existe
  if (fs.existsSync(fullPath)) {
    // Define cabeçalhos para o download
    res.setHeader('Content-Disposition', `attachment; filename=${path.basename(fullPath)}`);
    return res.status(200).sendFile(fullPath);
  } else {
    // Arquivo não encontrado
    return res.status(404).json({ message: 'Arquivo não encontrado' });
  }
}