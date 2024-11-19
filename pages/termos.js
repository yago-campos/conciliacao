// pages/termos.js
import React from 'react';
import Footer from '../components/Footer';

const TermsOfService = () => {
  return (
    <>
      <header>
        <h1>Termos de Serviço</h1>
      </header>
      <div className="terms-of-service">
        <h1></h1>
        <p>Atualizado em: Novembro de 2024</p>

        <section>
          <h2>1. Aceitação dos Termos</h2>
          <p>
            Ao acessar e utilizar nossos serviços, você concorda em cumprir e estar vinculado aos seguintes termos e condições. Se você não concordar com estes termos, não deve utilizar os serviços.
          </p>
        </section>

        <section>
          <h2>2. Uso dos Serviços</h2>
          <p>
            Você concorda em usar os serviços exclusivamente para fins legais e de acordo com as leis aplicáveis. Não é permitido utilizar os serviços para atividades ilícitas, prejudiciais ou fraudulentas.
          </p>
        </section>

        <section>
          <h2>3. Criação de Conta</h2>
          <p>
            Para acessar certos recursos dos nossos serviços, você pode ser solicitado a criar uma conta. Você é responsável por manter a confidencialidade de sua conta e informações de acesso. Caso perceba qualquer uso não autorizado de sua conta, deve nos notificar imediatamente.
          </p>
        </section>

        <section>
          <h2>4. Modificação dos Serviços</h2>
          <p>
            Reservamo-nos o direito de modificar, suspender ou descontinuar nossos serviços a qualquer momento, sem aviso prévio. Não nos responsabilizamos por qualquer interrupção ou falha nos serviços.
          </p>
        </section>

        <section>
          <h2>5. Propriedade Intelectual</h2>
          <p>
            Todos os conteúdos, marcas, logotipos e materiais disponíveis nos nossos serviços são propriedade nossa ou de nossos licenciadores. Nenhum conteúdo dos nossos serviços pode ser copiado, distribuído ou modificado sem autorização prévia.
          </p>
        </section>

        <section>
          <h2>6. Privacidade e Proteção de Dados</h2>
          <p>
            A coleta e o uso de seus dados pessoais são regidos pela nossa Política de Privacidade. Ao utilizar nossos serviços, você concorda com as práticas descritas nessa política.
          </p>
        </section>

        <section>
          <h2>7. Limitação de Responsabilidade</h2>
          <p>
            Não somos responsáveis por danos diretos, indiretos, incidentais ou consequenciais decorrentes do uso ou incapacidade de usar nossos serviços, mesmo que tenhamos sido avisados da possibilidade desses danos.
          </p>
        </section>

        <section>
          <h2>8. Indenização</h2>
          <p>
            Você concorda em indenizar e isentar nossos diretores, funcionários, afiliados e parceiros de qualquer reivindicação, responsabilidade, perda, dano ou despesa decorrente do seu uso dos serviços ou violação destes termos.
          </p>
        </section>

        <section>
          <h2>9. Alterações nos Termos</h2>
          <p>
            Podemos modificar esses Termos de Serviço a qualquer momento. A versão atualizada estará disponível nesta página e será válida a partir da data de publicação. Recomendamos que você revise os termos periodicamente.
          </p>
        </section>

        <section>
          <h2>10. Legislação Aplicável</h2>
          <p>
            Estes Termos de Serviço são regidos pelas leis do Brasil. Quaisquer disputas serão resolvidas nos tribunais da cidade de Curitiba.
          </p>
        </section>

        <section>
          <h2>11. Contato</h2>
          <p>
            Se você tiver dúvidas sobre estes Termos de Serviço ou precisar de mais informações, entre em contato conosco pelo e-mail: <a href="mailto:contato@exemplo.com">contato@exemplo.com</a>.
          </p>
        </section>
      </div>
      
    </>
  );
};

export default TermsOfService;