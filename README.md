# drawable-app

## Equipe
- Samuel Campos (Tyxiel)
- João Pedro Chaves
- João Victor

## Repositório
[Drawable APP](https://github.com/Tyxiel/drawable-app)

---

## Descrição do Sistema

O **drawable-app** é um aplicativo de desenho simples com interface gráfica (Tkinter) que permite criar figuras geométricas (linha, rabisco, retângulo, oval, círculo e polígonos regulares) com cores personalizáveis de borda e preenchimento.  
O projeto foi desenvolvido seguindo o padrão **MVC** (Model-View-Controller) e aplica princípios de **Orientação a Objetos**, com hierarquia de classes para as figuras.

**Funcionalidades:**
- Desenho interativo com pré-visualização tracejada.
- Escolha de cores de borda e preenchimento via seletor.
- Limpeza da cor de preenchimento.
- Desfazer (Ctrl+Z).
- **Persistência:** salvar e abrir desenhos em arquivos `.pkl`.

---

## Documentação

### Quantidade de classes documentadas
- **5 classes públicas**:
  - `Figura` (abstrata)
  - `Linha`
  - `Rabisco`
  - `Retangulo`
  - `Oval`
  - `Circulo`
  - `PoligonoRegular`
  - `DrawingModel`
  - `DrawingView`
  - `DrawingController`

> Total: **10 classes** documentadas com descrição, autor, versão e detalhamento de métodos.

### Quantidade de métodos documentados
- **Métodos públicos documentados**: aproximadamente **25** (incluindo construtores e métodos de instância).  
  Todos os métodos públicos possuem descrição, parâmetros (`@param`), retorno (`@return`) e exceções (`@throws`) quando aplicável.

### Como visualizar a documentação

1. Gere os arquivos HTML com Pydoc:
   ```bash
   pydoc -w src.figuras src.model src.view src.controller
   ```
2. Os arquivos HTML serão criados na raiz do projeto. Para organizá-los, mova-os para a pasta `docs/`:
   ```bash
   mkdir -p docs
   mv *.html docs/
   ```
3. Abra qualquer um dos arquivos no navegador, por exemplo:
   - `docs/src.figuras.html`
   - `docs/src.model.html`
   - etc.

Alternativamente, você pode gerar a documentação do pacote inteiro com:
```bash
pydoc -w src
```
E visualizar `src.html`.

---

## Instruções para executar

```bash
python main.py
```

---

## Tecnologias
- Python 3.x
- Tkinter (interface gráfica)
- Pickle (persistência)
- Pydoc (documentação)

---

## Licença
Projeto acadêmico – sem fins comerciais.