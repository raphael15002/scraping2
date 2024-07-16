from bs4 import BeautifulSoup
import requests
import warnings
import csv

warnings.filterwarnings("ignore")

codigo_tce = []
n_instrumento = []
ano = []
situacao = []
objeto = []
tipo_pessoa = []
meus_links = []
cpf_cnpj = []
nome_fornecedor = []
Razão_social = []

for i in range(0, 28):
    print(f"Página: {i + 1}\n")

    url = f"https://transparencia.tcerr.tc.br/contratacoes/contratos?instrumentoContratual=&ano=&objeto=&dataAssinaturaInicial=&dataAssinaturaFinal=&valorContratadoInicial=&valorContratadoFinal=&vigenciaInicial=&vigenciaFinal=&prazoFinalDaVigenciaInicial=&prazoFinalDaVigenciaFinal=&tipoDeInstrumentoContratualId=&situacaoId=&cpfCnpj=&nomeDoFornecedor=&tipoDeOrigemDoContratoId=&page={i + 1}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers, verify=False)

    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find_all("a", href=True)

    for j in content:
        if 'informacao-contrato/' in j['href']:
            meus_links.append(j['href'])
    
    print(f"Concluído: página {i + 1}")
    
url_root = 'https://transparencia.tcerr.tc.br{}'
for link in meus_links:
    try:
        response = requests.get(url_root.format(link), verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Função para extrair texto com verificação de presença
            def extract_text(soup, label_text):
                label = soup.find(text=label_text)
                if label:
                    sibling = label.find_next('p')
                    return sibling.text.strip() if sibling else None
                return None

            codigo_tce.append(extract_text(soup, "Código TCE:"))
            n_instrumento.append(extract_text(soup, "Número Instrumento:"))
            ano.append(extract_text(soup, "Ano:"))
            situacao.append(extract_text(soup, "Situação:"))
            objeto.append(extract_text(soup, "Objeto:"))
            tipo_pessoa.append(extract_text(soup, "Tipo de Pessoa:"))
            cpf_cnpj.append(extract_text(soup, "CPF/CNPJ:"))
            nome_fornecedor.append(extract_text(soup, "Nome Fornecedor:"))
            Razão_social.append(extract_text(soup, "Razão Social:"))
        else:
            print(f"Erro ao acessar o link: {link} - {response.status_code}")
    except Exception as e:
        print(f"Erro ao acessar o link: {link} - {str(e)}")

# Salvando os dados em um arquivo CSV
with open('contratos.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Código TCE', 'Número Instrumento', 'Ano', 'Situação', 'Objeto', 'Tipo Pessoa', 'Link', 'CPF/CNPJ', 'Nome Fornecedor', 'Razão Social'])
    for i in range(len(codigo_tce)):
        writer.writerow([codigo_tce[i], n_instrumento[i], ano[i], situacao[i], objeto[i], tipo_pessoa[i], meus_links[i], cpf_cnpj[i], nome_fornecedor[i], Razão_social[i]])

print("Dados salvos em contratos.csv")