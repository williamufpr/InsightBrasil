from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def generate_simple_pdf(filename="instrucoes.pdf"):
    """
    Gera um arquivo PDF simples com um título e texto de exemplo.

    Args:
        filename (str): O nome do arquivo PDF a ser gerado.
    """
    try:
        c = canvas.Canvas(filename, pagesize=letter)

        # Configurar fonte e tamanho para o título
        c.setFont("Helvetica-Bold", 24)
        c.drawString(inch, 10 * inch, "Como acessar o Storytelling") # Posição (x, y)

        # Configurar fonte e tamanho para o corpo do texto
        c.setFont("Helvetica", 12)
        
        # Inserir linhas de texto
        text_lines = [
            "Olá Dra.  como está ?",
            "Eu resolvi publicar o meu roteiro de storytelling num site",

            "", # Linha em branco
            "Basta acessar o link a seguir : ", 
            "http://trabalho-sto-william-alencar.streamlit.app",
            "Talvez seja necessário clicar no botão wake up para que o site seja carregado"
        ]
        
        # Posição inicial para o texto (logo abaixo do título)
        text_y_position = 9.0 * inch
        line_height = 0.2 * inch # Altura de cada linha de texto

        for line in text_lines:
            c.drawString(inch, text_y_position, line)
            text_y_position -= line_height # Move para a próxima linha

        # Opcional: Adicionar um rodapé
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(inch, 0.75 * inch, "Gerado automaticamente por Python")

        # Salvar o PDF
        c.save()
        print(f"PDF '{filename}' gerado com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro ao gerar o PDF: {e}")

if __name__ == "__main__":
    generate_simple_pdf()