# 🚀 Guia de Setup do Repositório IKEA India Case Study

## 📋 Pré-requisitos

- Conta no GitHub
- Git instalado localmente
- Editor de texto (VS Code recomendado)

---

## 🏗️ Passo a Passo para Criar o Repositório

### 1. Criar Repositório no GitHub

1. Acesse github.com e faça login
2. Clique em **"New repository"**
3. Configure:
   - **Repository name**: `ikea-india-case-study`
   - **Description**: `Strategic analysis of IKEA India's organizational alignment challenges using Deloitte-Marzo 9S Matrix`
   - **Visibility**: Public
   - ✅ **Add a README file** (vamos substituir depois)
   - **Add .gitignore**: None
   - **Choose a license**: MIT License (opcional)
4. Clique em **"Create repository"**

---

### 2. Clonar Repositório Localmente

```bash
git clone https://github.com/SEU-USERNAME/ikea-india-case-study.git
cd ikea-india-case-study
```

---

### 3. Criar Estrutura de Pastas

```bash
# Criar todas as pastas de uma vez
mkdir -p analysis data visuals references

# Verificar estrutura
tree -L 1
```

A estrutura deve ficar assim:
```
ikea-india-case-study/
├── analysis/
├── data/
├── visuals/
├── references/
└── README.md
```

---

### 4. Adicionar Arquivos

#### 4.1. README.md (principal)
- Copie todo o conteúdo do README que criei
- Cole no arquivo `README.md` na raiz do projeto
- **IMPORTANTE**: Atualize os links de contato no final:
  ```markdown
  [![LinkedIn](link-do-seu-linkedin)](seu-linkedin)
  [![Email](link-do-seu-email)](mailto:seu-email@exemplo.com)
  ```

#### 4.2. analysis/full-analysis-pt.md
- Copie todo o conteúdo da análise completa
- Salve em `analysis/full-analysis-pt.md`

#### 4.3. analysis/9s-framework-breakdown.md
Crie este arquivo com:

```markdown
# 9S Framework - Breakdown Detalhado

## Modelo 7S Original (McKinsey)

1. Strategy
2. Structure  
3. Systems
4. Skills
5. Staff
6. Style
7. Shared Values

## Adições de Marzo

8. **Stakeholders**: Captura relações e expectativas de partes interessadas externas
9. **Social Responsibility**: Integra compliance, sustentabilidade e impacto social

## Aplicação ao Caso IKEA India

[Incluir diagrama visual do 9S aplicado]

### Por Dimensão:

#### Strategy
- **Definição**: Direção e escopo de longo prazo
- **No caso IKEA**: Replicação de modelo europeu sem adaptação
- **Gap identificado**: Product-market fit inadequado

[Continue para cada dimensão...]
```

#### 4.4. analysis/flow-of-influence.md
```markdown
# Análise de Fluxo de Influência

## Cascata de Desalinhamento

### Fluxo Primário (Top-Down)

```
Strategy → Structure → Systems → Staff
```

### Fluxo Reverso (Bottom-Up)

```
Staff/Culture ← Shared Values ← Style ← Structure
```

### Pontos de Amplificação

1. **Strategy → Structure**: Ambiguidade decisória
2. **Structure → Systems**: Fragmentação operacional  
3. **Systems → Staff**: Rotatividade e perda de conhecimento
4. **Culture → Shared Values**: Silos informais

[Desenvolver cada ponto...]
```

#### 4.5. data/
- Salve o PDF original do caso como `case-study-original.pdf`
- Salve a tradução em português (se tiver) como `case-study-translated-pt.pdf`

#### 4.6. references/9s-matrix-methodology.md
```markdown
# Metodologia da Matriz 9S

## Origem

A Matriz 9S é uma evolução do modelo 7-S da McKinsey, expandida por Marzo para incluir dimensões críticas de stakeholders externos e responsabilidade social.

## Quando Usar

- Diagnósticos organizacionais abrangentes
- Análise de fusões e aquisições
- Expansões internacionais
- Transformações culturais

## Como Aplicar

### Passo 1: Mapeamento
Identificar estado atual de cada dimensão

### Passo 2: Gap Analysis  
Comparar com estado desejado

### Passo 3: Interdependências
Mapear como desalinhamentos se propagam

### Passo 4: Priorização
Definir ações por impacto e viabilidade

## Referências

- Waterman, R., Peters, T., & Phillips, J. (1980). Structure is not organization. Business Horizons, 23(3), 14-26.
- Marzo, G. (2015). Extension of the 7S Framework for Sustainability Contexts. [Fonte]
```

---

### 5. Adicionar Elementos Visuais (opcional)

Se você quiser criar os diagramas mencionados no README:

#### Ferramentas Recomendadas:
- **Mermaid Live Editor**: mermaid.live (já usei no README)
- **Canva**: para infográficos
- **Excalidraw**: para diagramas manuais
- **Draw.io**: para fluxogramas

#### Imagens Sugeridas:
1. `visuals/9s-framework-diagram.png` - Diagrama do framework
2. `visuals/misalignment-cascade.png` - Cascata de desalinhamento
3. `visuals/recommendations-roadmap.png` - Timeline de recomendações

---

### 6. Commit e Push

```bash
# Adicionar todos os arquivos
git add .

# Verificar o que será commitado
git status

# Fazer commit
git commit -m "Initial commit: IKEA India case study analysis using 9S Matrix"

# Enviar para GitHub
git push origin main
```

---

### 7. Configurações Adicionais no GitHub

#### 7.1. Topics (Tags)
No repositório do GitHub, adicione estas tags:
- `case-study`
- `organizational-analysis`
- `strategic-management`
- `9s-matrix`
- `ikea`
- `india-market`
- `change-management`

#### 7.2. About
Adicione a descrição:
```
Strategic analysis of IKEA India's organizational alignment challenges using Deloitte-Marzo 9S Matrix. Demonstrates analytical thinking and structured problem-solving approach.
```

#### 7.3. GitHub Pages (opcional)
Para criar um site do seu caso:

1. Vá em **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **main** / **root**
4. Save

Seu README será renderizado em: `https://seu-username.github.io/ikea-india-case-study/`

---

### 8. Adicionar Badge Customizado (opcional)

Crie um badge mostrando que é um case study:

```markdown
![Case Study](https://img.shields.io/badge/Type-Case%20Study-blue?style=flat-square)
![Framework](https://img.shields.io/badge/Framework-9S%20Matrix-orange?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-success?style=flat-square)
```

---

## ✅ Checklist Final

Antes de compartilhar o repositório, verifique:

- [ ] README.md está completo e formatado
- [ ] Links de contato atualizados
- [ ] Todos os arquivos markdown sem erros de formatação
- [ ] Estrutura de pastas correta
- [ ] Commits com mensagens descritivas
- [ ] Repositório público (se for compartilhar)
- [ ] Topics/tags adicionadas
- [ ] Descrição do repositório configurada
- [ ] Licença escolhida (se aplicável)

---

## 💡 Dicas Extras

### Para Impressionar Ainda Mais

1. **GitHub Actions**: Configure um workflow para validar markdown
2. **Issues Template**: Crie template para discussões sobre o caso
3. **Contributing Guide**: Adicione `CONTRIBUTING.md` se quiser colaborações
4. **Wiki**: Use a Wiki do GitHub para documentação adicional
5. **Projects**: Crie um board mostrando evolução da análise

### Exemplo de GitHub Action (opcional)

Crie `.github/workflows/markdown-lint.yml`:

```yaml
name: Markdown Lint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: avto-dev/markdown-lint@v1
        with:
          args: '**/*.md'
```

---

## 🎓 Resultado Final

Seu repositório estará pronto para:
- ✅ Ser incluído no portfólio
- ✅ Compartilhar com recrutadores
- ✅ Demonstrar capacidade analítica
- ✅ Mostrar proficiência técnica (Git, Markdown, documentação)

---

## 🆘 Problemas Comuns

### Erro ao fazer push
```bash
# Solução: Configurar credenciais
git config --global user.name "Seu Nome"
git config --global user.email "seu-email@exemplo.com"
```

### Imagens não aparecem no GitHub
- Verifique se o caminho está correto: `![alt](./visuals/imagem.png)`
- Certifique-se de que fez commit das imagens

### Mermaid não renderiza
- GitHub suporta Mermaid nativamente em blocos de código com ```mermaid
- Se não funcionar, use Mermaid Live Editor e exporte como imagem

---

## 📞 Suporte

Se tiver dúvidas durante o setup:
1. Consulte [GitHub Docs](https://docs.github.com)
2. Use [Stack Overflow](https://stackoverflow.com) para problemas técnicos
3. Veja exemplos em repositórios similares

---

**Boa sorte com seu repositório! 🚀**