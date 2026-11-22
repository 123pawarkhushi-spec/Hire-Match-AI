
import pymupdf


# --------------------------------------------------
# PDF RESUME TEXT EXTRACTION
# --------------------------------------------------

def extract_resume_text(pdf_file):

    try:

        pdf_data = pdf_file.read()

        if not pdf_data:

            raise ValueError("The uploaded PDF file is empty.")

        # Open PDF from memory
        doc = pymupdf.open(
            stream=pdf_data,
            filetype="pdf"
        )

        # Verify that PDF contains pages
        if doc.page_count == 0:

            doc.close()

            raise ValueError("The PDF contains no pages.")

        text = ""

        # Extract text from every page
        for page in doc:

            text += page.get_text() + "\n"

        doc.close()

        # Detect scanned or textless PDFs
        if not text.strip():

            raise ValueError(
                "No readable text found. "
                "This may be a scanned PDF."
            )

        return text

    except ValueError:

        raise

    except Exception as e:

        raise ValueError(
            f"Unable to read this PDF file: {e}"
        )
