# Lab CoAP com Docker e Wireshark

## Objetivo

Montar um lab local no Ubuntu com dois containers Docker usando o protocolo CoAP, um como **servidor** e outro como **cliente**, e acompanhar o tráfego no Wireshark.

## O que foi feito

### 1. Estrutura inicial do lab

Criei uma topologia simples com:

- `coap-server`: container que expõe um recurso CoAP.
- `coap-client`: container que faz requisições para o servidor.

A ideia era validar comunicação CoAP dentro da rede do Docker e observar os pacotes no host Ubuntu.

### 2. O CoAPthon

Para simplificar o lab, usei a implementação do **CoAPthon**.

Com isso:

- o servidor passou a escutar em `0.0.0.0:5683`;
- o cliente passou a falar com o servidor via UDP;
- o ambiente ficou mais simples para depuração e captura no Wireshark.

### 5. Lab funcionando

O client passou a receber resposta corretamente, mostrando algo como:

- `Code: 69`
- `Payload: 2026-04-15 20:26:01`

Isso confirmou que:

- o servidor CoAP estava respondendo;
- o cliente estava conseguindo acessar o recurso `/time`;
- a comunicação entre containers estava OK.

### 7. Cliente em loop

Depois, ajustei o client para enviar requisições repetidas a cada 1 segundo.

Isso foi útil para:

- manter o container ativo;
- gerar tráfego contínuo;
- facilitar a observação dos pacotes no Wireshark.

### 8. Captura no Wireshark

Para capturar o tráfego, vi que a melhor interface no Ubuntu é normalmente:

- `docker0`;
- ou a bridge criada pelo Compose, como `br-64e0306b5254`;
- `any` pode ser usada como teste.

Isso ajuda a enxergar o tráfego CoAP entre os containers.

### 9. Acesso ao container

Ao no container que está rodando o client usando `docker exec -it ID /bin/bash`.

Exemplo:

```bash
docker exec -it ID /bin/bash
```


Isso permite inspecionar o ambiente por dentro.

## Resumo técnico

### Componentes

- Docker.
- Docker Compose.
- Python.
- CoAPthon.
- Wireshark.

### Fluxo final

1. Subir os containers com `docker compose up --build`.
2. O servidor escuta na porta UDP 5683.
3. O cliente faz GET em `/time`.
4. O cliente repete a requisição a cada segundo.
5. O tráfego é capturado no Wireshark na interface do Docker.

## Conclusão

No fim, o lab ficou funcional para estudo de CoAP em Docker e análise de tráfego no Wireshark.