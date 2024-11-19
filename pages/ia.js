import React, { useState, useEffect, useRef } from "react";

const Chatbot = () => {
  const [messages, setMessages] = useState([]); // Histórico de mensagens
  const [input, setInput] = useState(""); // Entrada do usuário
  const [conversationContext, setConversationContext] = useState(null); // Contexto da conversa

  const chatWindowRef = useRef(null); // Referência para a janela do chat

  // Função para lidar com envio de mensagens
  const handleSend = () => {
    if (input.trim() === "") return; // Ignora mensagens vazias

    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);

    // Simulação de resposta da IA
    setTimeout(() => {
      const botMessage = { sender: "bot", text: getResponse(input) };
      setMessages((prev) => [...prev, botMessage]);
    }, 1000); // Simula 1 segundo de "processamento"

    setInput(""); // Limpa o campo de entrada
  };

  function getResponse(input) {
    const lowerInput = input.toLowerCase().trim(); // Converte para minúsculas e remove espaços extras
  
    // Verifica se há contexto ativo
    if (conversationContext === "conciliação") {
      if (/sim|quero|preciso/i.test(lowerInput)) {
        setConversationContext("detalhes_conciliação"); // Atualiza o contexto para esperar detalhes
        return "Ótimo! Por favor, me informe os detalhes do caso para que eu possa ajudar.";
      } else if (/não|obrigado/i.test(lowerInput)) {
        setConversationContext(null); // Reseta o contexto após a resposta
        return "Sem problemas! Estou por aqui se precisar de mais alguma coisa.";
      }
    }
  
    if (conversationContext === "detalhes_conciliação") {
      // Fluxo quando o usuário está dando mais detalhes
      if (/como|funciona|processo|passo/i.test(lowerInput)) {
        return "opa"; // Resposta para o exemplo fornecido
      }
      setConversationContext(null); // Reseta o contexto após essa interação
      
    }
  
    // Respostas padrão
    if (/olá|oi|opa|e aí/.test(lowerInput)) {
      return "Olá, Funcionauta! Como posso ajudar você hoje?";
    } else if (lowerInput.includes("tchau")) {
      return "Até logo! Volte sempre que precisar.";
    } else if (lowerInput.includes("eficiência")) {
      return "O time de Eficiência Operacional é o melhor!";
    } else if (lowerInput.includes("extrair relatório de ressarcimento")) {
      return "Para extrair o relatório de ressarcimento, acesse o portal da empresa e navegue até a seção 'Relatórios'.";
    } else if (lowerInput.includes("conciliação")) {
      setConversationContext("conciliação"); // Define o contexto para conciliação
      return "Conciliação é essencial para garantir que os valores estejam corretos. Deseja ajuda com algum caso específico?";
    } else if (lowerInput.includes("cash")) {
      return "Cash é uma parte importante da operação. Posso ajudar você com informações financeiras ou fluxo de caixa?";
    } else if (lowerInput.includes("pedido rejeitado")) {
      return "Pedidos rejeitados podem ser consultados no sistema de pedidos. Verifique os status e me avise se precisar de suporte.";
    }
  
    return "Desculpe, não entendi sua mensagem.";
  }

  // Efeito para descer automaticamente o scroll da janela do chat
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages]); // Executa toda vez que a lista de mensagens é atualizada

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>Pergunte à IA</h1>
      <div ref={chatWindowRef} style={styles.chatWindow}>
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              ...styles.message,
              alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
              backgroundColor: msg.sender === "user" ? "#daf8e3" : "#f0f0f0",
            }}
          >
            {msg.text}
          </div>
        ))}
      </div>
      <div style={styles.inputContainer}>
        <input
          type="text"
          placeholder="Digite sua mensagem..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={styles.input}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button onClick={handleSend} style={styles.button}>
          Enviar
        </button>
      </div>
    </div>
  );
};

// Estilos em linha
const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    height: "100vh",
    backgroundColor: "#f4f4f9",
  },
  header: {
    fontSize: "24px",
    marginBottom: "20px",
  },
  chatWindow: {
    width: "90%",
    maxWidth: "600px",
    height: "400px",
    border: "1px solid #ccc",
    borderRadius: "10px",
    padding: "10px",
    display: "flex",
    flexDirection: "column",
    overflowY: "auto", // Garante que o conteúdo possa rolar
    backgroundColor: "#fff",
  },
  message: {
    maxWidth: "70%",
    margin: "5px 0",
    padding: "10px",
    borderRadius: "8px",
    fontSize: "14px",
    wordBreak: "break-word",
  },
  inputContainer: {
    display: "flex",
    marginTop: "10px",
    width: "90%",
    maxWidth: "600px",
  },
  input: {
    flex: 1,
    padding: "10px",
    border: "1px solid #ccc",
    borderRadius: "4px",
    fontSize: "16px",
  },
  button: {
    marginLeft: "10px",
    padding: "10px 20px",
    backgroundColor: "#4CAF50",
    color: "#fff",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  },
};

export default Chatbot;