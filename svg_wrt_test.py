import svgwrite


def main():
    dwg = svgwrite.Drawing("test.svg", size=("500", "500"))
    svg_path = dwg.path(d="M 10 10 H 110 V 110 H 10 V 10", fill="none", stroke="green")
    dwg.add(svg_path)
    dwg.save(pretty=True)


if __name__ == "__main__":
    main()
