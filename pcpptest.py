from PCPartPicker_API import pcpartpicker as pcpp


mobo_count = pcpp.productLists.totalPages("motherboard")
print("Total Mobo pages:", mobo_count)

#Pull info from page 1 of CPUs
for page in range(0, 1):
    skuName = pcpp.productLists.getProductList("motherboard", page)
    # Print the names and prices of all the CPUs on the page
    for mobo in skuName:
        vendor = str(mobo["name"]).split(" ")
        print(vendor[0])
