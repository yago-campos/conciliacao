const express = require('express');
const connection = require('./db'); // Importa a conexão configurada

const router = express.Router();

// Rota para buscar dados do Snowflake
router.get('/dados', (req, res) => {
    connection.execute({
        sqlText: 'SELECT * FROM usuarios', // Ajuste conforme necessário
        complete: (err, stmt, rows) => {
            if (err) {
                console.error('Erro ao executar consulta:', err.message);
                res.status(500).send('Erro ao buscar dados.');
            } else {
                res.json(rows); // Retorna os dados como JSON
            }
        },
    });
});

module.exports = router;