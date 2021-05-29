from pymed import PubMed
pubmed = PubMed(tool="MyTool", email="lgs@unam.mx")
results = pubmed.query("fractal", max_results=500)
print(results)



