import React, { useState } from 'react';
import Link from 'next/link'; // Caso use Next.js

const Home = () => {
  const [industria, setIndustria] = useState('');
  const [distribuidor, setDistribuidor] = useState('');
  const [mensagem, setMensagem] = useState('');
  const [baseFuncionalFile, setBaseFuncionalFile] = useState(null);
  const [baseDistribuidorFile, setBaseDistribuidorFile] = useState(null);
  const [pfMargemFile, setPfMargemFile] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState(''); // Estado para a URL de download

  const handleConciliacao = async () => {
    setMensagem('Processando, por favor aguarde...');
    setDownloadUrl(''); // Limpa URL de download antes de começar o processo

    const formData = new FormData();
    formData.append('industria', industria);
    formData.append('distribuidor', distribuidor);
    formData.append('baseFuncional', baseFuncionalFile);
    formData.append('baseDistribuidor', baseDistribuidorFile);

    if (industria === 'msd' && distribuidor === 'gsc' && pfMargemFile) {
      formData.append('pfMargem', pfMargemFile);
    }

    try {
      const response = await fetch('/api/concilia', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        if (data.downloadUrl) {
          setDownloadUrl(data.downloadUrl); // Define a URL de download se estiver presente
          setMensagem('Conciliação realizada com sucesso!');
        } else {
          setMensagem('Erro: URL de download não encontrada.');
        }
      } else {
        const errorResponse = await response.json();
        setMensagem(errorResponse.error || 'Erro ao realizar conciliação.');
      }
    } catch (error) {
      console.error(error);
      setMensagem('Erro de conexão.');
    }
  };

  return (
    <div>


      <header>
        <h1>Processo de Conciliação</h1>
      </header>
      <main>
        <section className="intro">
          <h2>Conciliação de Ressarcimento</h2>
          <p>Preencha as informações para realizar a conciliação:</p>
          <div className="form">
            <label>
              Indústria:
              <select value={industria} onChange={(e) => setIndustria(e.target.value)}>
                <option value="">Selecione</option>
                <option value="organon">Organon</option>
                <option value="msd">MSD</option>
                <option value="sanofi">Sanofi</option>
                <option value="apsen">Apsen</option>
                <option value="bayer">Bayer</option>
              </select>
            </label>

            {industria && (
              <label>
                Distribuidor:
                <select value={distribuidor} onChange={(e) => setDistribuidor(e.target.value)}>
                  <option value="">Selecione</option>
                  {industria === 'organon' && <option value="gsc">GSC</option>}
                  {industria === 'apsen' && (
                    <>
                      <option value="dimed">Dimed</option>
                      <option value="gam">GAM</option>
                      <option value="gsc">GSC</option>
                      <option value="gjb">GJB</option>
                    </>
                  )}
                  {industria === 'msd' && (
                    <>
                      <option value="gsc">GSC</option>
                      <option value="agille">Agille</option>
                    </>
                  )}
                </select>
              </label>
            )}

            <label>
              Base Funcional:
              <input type="file" onChange={(e) => setBaseFuncionalFile(e.target.files[0])} />
            </label>

            <label>
              Base Distribuidor:
              <input type="file" onChange={(e) => setBaseDistribuidorFile(e.target.files[0])} />
            </label>

            {industria === 'msd' && distribuidor === 'gsc' && (
              <label>
                Arquivo PF Margem:
                <input type="file" onChange={(e) => setPfMargemFile(e.target.files[0])} />
              </label>
            )}

            <button onClick={handleConciliacao}>Iniciar Conciliação</button>
            <p>{mensagem}</p>

            {/* Exibe o botão de download se a URL estiver disponível */}
            {downloadUrl ? (
              <a href={downloadUrl} download="resultado_conciliacao.xlsx">
                <button>Baixar Resultado</button>
              </a>
            ) : (
              <p></p>
            )}
          </div>
        </section>
      </main>

      <style jsx>{`
        nav.menu {
          background-color: #333;
          color: white;
          padding: 10px;
        }

        nav.menu ul {
          display: flex;
          justify-content: space-around;
          list-style: none;
          margin: 0;
          padding: 0;
        }

        nav.menu ul li a {
          color: white;
          text-decoration: none;
          font-weight: bold;
        }

        nav.menu ul li a:hover {
          text-decoration: underline;
        }

        header {
          background-color: #4CAF50;
          color: white;
          padding: 20px;
          text-align: center;
        }

        main {
          text-align: center;
          padding: 20px;
          background-color: #f9f9f9;
        }

        .intro {
          padding: 20px;
          background-color: #fff;
          border-radius: 10px;
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
          margin-bottom: 20px;
        }

        .form {
          display: flex;
          flex-direction: column;
          gap: 10px;
          text-align: left;
          max-width: 400px;
          margin: 0 auto;
        }

        .form label {
          font-size: 16px;
        }

        .form select,
        .form input,
        .form button {
          padding: 8px;
          font-size: 16px;
        }

        button {
          background-color: #4CAF50;
          color: white;
          border: none;
          padding: 10px;
          cursor: pointer;
          border-radius: 5px;
          font-size: 16px;
        }

        button:hover {
          background-color: #388E3C;
        }
      `}</style>
    </div>
  );
};

export default Home;
