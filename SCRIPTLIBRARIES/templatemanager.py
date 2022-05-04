class template_manager:
    def __init__(self):
        self.templatedata = ""


    def load_html_template(self,path):
        f = open(path, "r")
        tempdata = f.read()
        f.close()
        self.templatedata = tempdata

    def format_html(self,substitute_array=[],encode_value="{aa}"):
        # Loop through all the elements in substitute_array to parse each value into a single position of the encoding value
        for i in substitute_array:
            if encode_value in i:
                raise TypeError("You Cant use the encoding value as part of the htmldata!")
            self.templatedata = self.templatedata.replace(encode_value,i,1)
    
    def get_parsed_html(self):
        return (self.templatedata)