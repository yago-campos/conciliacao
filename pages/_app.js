// pages/_app.js

import '../styles/style.css';  // Importa os estilos globais aqui
// import Footer from '../components/Footer';  // Importe o Footer


function MyApp({ Component, pageProps }) {
  return (
    <>
      {/*<Header />   Exibe o Header */}
      <Component {...pageProps} />  {/* Exibe o conteúdo da página */}
      
    </>
  );
}

export default MyApp;