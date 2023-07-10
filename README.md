# SASVP
### Sistema de Acompanhamento Vocal da Saúde de Professores
 
 Este é um Projeto da Disciplina de de Arquitetura de Computadores, do IFPB, sob a orientação do Professor Michel Coura Dias

 ## Motivação

 - Os Professores estão em um conjunto de profissionais que mais fazem uso da voz.​

 - O uso intensivo, o estresse e a alta exposição a ruído são alguns dos fatores causadores dos problemas vocais em professores e objetos de estudos.

 ## Escopo *back-end*

 - Definição do modelo para triagem automática:​
   - Base de dados​
   - Características acústicas​
   - Treinamento e validação​
   - Obtenção do modelo após o teste

 ## Escopo *front-end*

 - Acesso do usuário (professor)​
   - Acesso​
   - Gravação do áudio​
   - Informações ao "paciente"​

 - Acesso do usuário (fono)​
   - Acesso ao banco de dados​
   - Dashboard de casos críticos por paciente.
  
 ## Aspectos de Desenvolvimento

 - Fase back-end:
   - Banco de dados de referência: Kay Elemetrics, 1994. Paradigma saudável (SDL) versus patológico (PTL);​​
   - Aplicação de AI com abordagem Deep Learning (treino, validação e teste do modelo) - TensorFlow;​​
   - Ideia do modelo: calcular a probabilidade do Professor possuir uma patologia laríngea.​​

 ## Requisitos de Projeto

 - Bibliotecas Python:
   - Sys​
   - Os​
   - Glob​
   - datetime == 5.1​
   - matplotlib == 3.7.1​
   - pandas == 1.4.2​
   - numpy == 1.22.4​
   - scipy == 1.10.1​
   - soundfile == 0.12.1​
   - PyQt5 == 5.15.9​
   - sounddevice == 0.4.6​
   - praat-parselmouth == 0.4.3​
   - tensorflow == 2.12.0​
   - librosa == 0.10.0

 - S.O.: Windows ou Linux​
   - Dual-core (min)​
   - 4 GB RAM (min)

 - Equipamentos adicionais:
   - Microfone​
   - Interface básica de áudio​
   - Preferencialmente uma sala preparada para a coleta.