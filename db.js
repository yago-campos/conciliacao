const snowflake = require('snowflake-sdk');

// Configuração da conexão
const connection = snowflake.createConnection({
    account: 'xzqggdu-fua20629',
    username: 'yagocampos',
    password: 'R4tF1sh3r$Snowflake',
    warehouse: 'DEV',
    database: 'DEV_DB',
    schema: 'PUBLIC',
});

// Testa a conexão ao inicializar
connection.connect((err) => {
    if (err) {
        console.error('Erro ao conectar ao Snowflake:', err.message);
    } else {
        console.log('Conexão com Snowflake estabelecida!');
    }
});

module.exports = connection;