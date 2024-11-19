const path = require('path');

module.exports = {
  api: {
    bodyParser: {
      sizeLimit: '20mb', // Definindo o limite de tamanho do body para 20 MB
    },
  },
  async rewrites() {
    return [
      {
        source: '/uploads/:path*', // URL pública
        destination: '/api/uploads/:path*', // Rota para o endpoint
      },
    ];
  },
};