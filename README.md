# **Professor I.S.A.A.C.**

**Professor I.S.A.A.C.** é uma aplicação de Inteligência Artificial interativa que processa perguntas por voz, responde usando GPT-4, captura e processa imagens, além de sintetizar respostas em áudio. A interação é feita via teclado, onde o usuário pode iniciar gravações e obter respostas através de atalhos de teclado.

Para mais projetos e ferramentas com Python, acesse a [Asimov Academy](https://hub.asimov.academy/curso/atividade/boas-vindas/).  
Veja o código completo do projeto neste [vídeo]( LINK ).

## **Instalação**

### **1. Requisitos**

- Python 3.11
- [Poetry](https://python-poetry.org/docs/#installation) para gerenciamento de dependências
- Microfone e alto-falantes
- Câmera IP ou webcam para capturas de imagens

### **2. Clone o Repositório**

```sh
git clone https://github.com/asimov-academy/professor-isaac.git
cd professor-isaac
```

### **3. Instale as Dependências**

Execute o comando abaixo para instalar as dependências listadas no arquivo `pyproject.toml`:

```sh
poetry install
```

### **4. Configure as Variáveis de Ambiente**

Crie um arquivo `.env` na raiz do projeto e adicione sua chave da API do OpenAI:

```sh
OPENAI_API_KEY="SUA-API-KEY-DA-OPENAI-AQUI"
```

## **Uso**

### **1. Descrição do Projeto**

O **Professor I.S.A.A.C.** é uma IA com funcionalidade de captura de imagem e gravação de voz para a simulação de uma interação com um professor.
Utilizando o modelo GPT-4o-mini para a obtenção de respostas.

#### Principais Funcionalidades:
- **Interação por Voz**: O sistema transcreve as perguntas feitas e responde utilizando inteligência artificial.
- **Respostas em Tempo Real**: Utiliza o modelo GPT-4 para gerar respostas didáticas e interativas.
- **Síntese de Voz**: As respostas são convertidas em fala e reproduzidas em tempo real.
- **Captura e Processamento de Imagens**: Imagens são capturadas da câmera e descritas em texto.

### **2. Como Funciona**

1. **Atalhos de Teclado**: A interação é feita através dos seguintes atalhos:
   - Pressione `V` para iniciar a gravação de voz.
   - Pressione `F` para enviar a pergunta e obter a resposta.
   - Pressione `Q` para encerrar a aplicação.

2. **Captura de Imagem**: O sistema captura imagens de uma câmera IP ou webcam, que são processadas e descritas como parte da resposta.

3. **Respostas Inteligentes**: O sistema usa GPT-4 para gerar respostas baseadas no contexto da pergunta e nas imagens capturadas.


### **3. Executando o Projeto**

Para iniciar o **Professor I.S.A.A.C.**, execute:

```sh
poetry run python main.py
```

### **4. Estrutura do Código**

- **ProfessorISAAC**: Classe principal que lida com a captura de imagem, reconhecimento de voz e processamento de perguntas.
- **speak()**: Função que converte texto em fala utilizando o modelo TTS.
- **frame_capture()**: Captura frames da câmera para processamento.
- **obter_resposta()**: Envia a pergunta ao modelo GPT-4 e retorna a resposta.
- **transcribe_audio()**: Transcreve o áudio capturado usando Whisper.
- **hear()**: Monitora o microfone para gravação de áudio e obtém perguntas.
- **start_listening()**: Inicia a escuta do áudio do usuário.
- **stop_listening_and_get_response()**: Para a escuta e envia a pergunta ao GPT-4.

### **5. Referências e Recursos**

- [OpenAI API](https://beta.openai.com/docs/)
- [Langchain](https://python.langchain.com/docs/)
- [Faster Whisper](https://github.com/guillaumekln/faster-whisper)
- [Pillow](https://python-pillow.org/)
- [Poetry](https://python-poetry.org/)


## **Licença**

Este projeto está licenciado sob a Licença **Asimov Academy**.
