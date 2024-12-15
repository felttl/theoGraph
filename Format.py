

class Graph:

    supported_formats = [
        "json", "csv"
    ]

    def __init__(self, data:list, format:str="json"):
        """nodes represents the tree itself 
        (etc... representes others nodes or elements added if necessary)        
        with the following format (json format or csv format) :         
            json format : 
        [
            master_node_1: [child_1, child_2, etc...],
            master_node_2: [child_1,child_2, etc... ],
            etc...
        ]

        example : 

        - json :
        [
            "a": ["b", "c", "d"],
            "b": ["b", "c"],
            "c": ["a", "b", "e"]
        ]
        - csv :
        [
            "a","b","c","d","e"
            "b","c","d"
            "b","c"
            "a","b","e"
        ]
        
        """
        self.adj = []
        # check if good format :
        if(not Graph.format_match(format)):
            raise Exception(f'format : "{format}" is not supported ({Graph.supported_formats})')
        
    
    @staticmethod
    def format_match(format:str) -> bool:
        """test si le format est supporté ou non"""
        count = -1
        found = False
        while not found & count < len(Graph.supported_formats) & format != "" & format != None:
            count += 1
            if(format == Graph.supported_formats[count]):
                found = True
        return found

# inheritance if oriented or not


# end