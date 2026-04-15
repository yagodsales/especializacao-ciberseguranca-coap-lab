# Guia de Laboratório: Protocolo CoAP com Máquinas Virtuais e Contiki-NG

Este documento descreve dois métodos para montar um ambiente de testes para o protocolo CoAP (Constrained Application Protocol).

---

## 1. Laboratório com Máquinas Virtuais (VirtualBox ou VMware)
*Focado em simular a comunicação entre sistemas operacionais completos ou Gateways.*

### Pré-requisitos
*   **Virtualizador:** VirtualBox ou VMware.
*   **SO:** 2 VMs Linux (Ubuntu/Debian).
*   **Rede:** Ambas em modo **Placa Bridge** ou **Rede Interna** (mesmo segmento).
 
### Passo a Passo
1.  **Instalação (em ambas as VMs):**
    ```bash
    sudo apt update
    sudo apt install python3-pip -y
    pip install aiocoap[all]
    ```

2.  **Configuração do Servidor (VM 1):**
    Crie o arquivo `server.py`:
    ```python
    import asyncio
    import aiocoap.resource as resource
    import aiocoap

    class StatusResource(resource.Resource):
        async def render_get(self, request):
            return aiocoap.Message(payload=b"Servidor CoAP Ativo!")

    async def main():
        root = resource.Site()
        root.add_resource(['status'], StatusResource())
        await aiocoap.Context.create_server_context(root)
        await asyncio.get_running_loop().create_future()

    if __name__ == "__main__":
        asyncio.run(main())
    ```
    Execute: `python3 server.py`

3.  **Teste do Cliente (VM 2):**
    Substitua `<IP_DA_VM1>` pelo endereço real da VM servidora:
    ```bash
    aiocoap-client get coap://<IP_DA_VM1>/status
    ```

---

## 2. Laboratório com Contiki-NG e Cooja
*Focado em simular redes de sensores de baixo consumo (IoT) e protocolos de malha (Mesh).*

### Pré-requisitos
*   **Docker** instalado na máquina hospedeira.

### Passo a Passo
1.  **Baixar Imagem:**
    ```bash
    docker pull contiker/contiki-ng
    ```

2.  **Iniciar o Cooja:**
    ```bash
    docker run --privileged -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix contiker/contiki-ng
    # No terminal do container:
    cd tools/cooja
    ant run
    ```

3.  **Configurar Simulação:**
    *   **File > New Simulation:** Dê um nome e crie.
    *   **Servidor:** Motes > Add Motes > Create New Mote Type > Sky Mote. Selecione o código em `/examples/coap/coap-example-server/`. Compile e adicione 1 unidade.
    *   **Cliente:** Repita o processo usando o código em `/examples/coap/coap-example-client/`.
    *   **Execução:** Clique em **Start**. Acompanhe os logs na janela *Mote Output*.

---

## 3. Monitoramento de Rede
Para analisar os pacotes em qualquer um dos cenários:
1.  Abra o **Wireshark**.
2.  Selecione a interface de rede do laboratório.
3.  Aplique o filtro: `coap`.
4.  Observe os campos: *Confirmable (CON)*, *Code (GET/POST)*, *Token* e *Payload*.
