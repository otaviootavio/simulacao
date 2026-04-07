# Simulação

Documento LaTeX (`main.tex`).

## Compilar

É preciso ter uma distribuição TeX instalada (por exemplo [TeX Live](https://www.tug.org/texlive/) no Linux).

No diretório do projeto:

```bash
pdflatex main.tex
```

O PDF gerado fica em `main.pdf`. Se o editor rodar `pdflatex` mais de uma vez para atualizar referências, repita o comando ou use `latexmk -pdf main.tex` se tiver o `latexmk` instalado.
