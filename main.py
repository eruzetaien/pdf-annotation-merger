from pikepdf import Pdf

def combine_annotations(original_path, copy_path, output_path):
    pdf_target = Pdf.open(original_path)
    pdf_source = Pdf.open(copy_path)

    for i, page_target in enumerate(pdf_target.pages):
        if i >= len(pdf_source.pages):
            break

        page_source = pdf_source.pages[i]

        source_annots = page_source.get("/Annots")

        if not source_annots:
            continue

        if "/Annots" not in page_target:
            page_target["/Annots"] = pdf_target.make_indirect([])

        target_annots = page_target["/Annots"]

        for annot in source_annots:
            try:
                copied_annot = pdf_target.copy_foreign(annot)
                target_annots.append(copied_annot)
            except Exception as e:
                print(f"Skip annot on page {i}: {e}")

    pdf_target.save(output_path)
    print(f"Done! Saved to {output_path}")


def main():
    filepath_1 = "original.pdf"
    filepath_2 = "copy.pdf"
    combine_annotations(filepath_1, filepath_2 , "final_combined.pdf")

if __name__ == "__main__":
    main()
