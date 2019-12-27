"""
Helper set functions for optAI
"""


ALL_DOMAINS = ['int', 'ric', 'term-int',
                'dis-int', 'term-dis-int', 'boxes',  
                'zones', 'oct', 'pk', 
                'as-int', 'as-ric', 'as-term-int', 
                'as-dis-int', 'as-term-dis-int', 'as-boxes', 
                'as-zones', 'as-oct', 'as-pk',
                'bool']


def set_difference(a, b):
    return [x for x in a if x not in b]

def set_union(a, b):
    c = set_difference(b, a)
    return a + c

all_incomparable_elements = { 
                                "pk" : ["bool","term-int", "ric", "dis-int", "boxes", "term-dis-int"],
                                "oct" : ["bool", "term-int", "ric", "dis-int", "boxes", "term-dis-int"],
                                "zones" : ["bool", "term-int", "ric", "dis-int", "boxes", "term-dis-int"],
                                "term-int" : ["pk", "oct", "zones", "ric", "dis-int", "boxes", "bool", "term-dis-int"],
                                "ric" : ["pk", "oct", "zones", "term-int", "dis-int", "boxes", "term-dis-int", "bool"], 
                                "dis-int" : ["pk", "oct", "zones", "term-int", "ric", "bool"],
                                "boxes" : ["pk", "oct", "term-int", "ric", "term-dis-int", "bool"],
                                "term-dis-int" : ["pk", "oct", "zones", "term-int", "ric", "boxes", "bool"],
                                "bool" : ["pk", "oct", "zones", "term-int", "int", "ric", "boxes", "dis-int", "term-dis-int"],
                                "int" : ["bool"]
                            }

all_comparable_elements = {
                                "pk" : ["oct", "zones", "int"],
                                "oct" : ["pk", "zones", "int"],
                                "zones" : ["pk", "oct", "int"],
                                "int" : ["pk", "oct", "zones", "term-int", "ric", "dis-int", "boxes", "term-dis-int"],
                                "term-int" : ["int"],
                                "ric" : ["int"],
                                "dis-int" : ["int", "boxes", "term-dis-int"],
                                "boxes" : ["dis-int", "int"],
                                "term-dis-int" : ["dis-int", "int"],
                                "bool" :  []
                        }

array_normalizer = {
                    "int" : "int",
                    "ric" : "ric",
                    "term-int" : "term-int",
                    "dis-int" : "dis-int", 
                    "term-dis-int" : "term-dis-int", 
                    "boxes" : "boxes",  
                    "zones" : "zones", 
                    "oct" : "oct", 
                    "pk" : "pk", 
                    "as-int" : "int", 
                    "as-ric" : "ric", 
                    "as-term-int" : "term-int", 
                    "as-dis-int" : "dis-int", 
                    "as-term-dis-int" : "term-dis-int", 
                    "as-boxes" : "boxes", 
                    "as-zones" : "zones", 
                    "as-oct" : "oct", 
                    "as-pk" : "pk", 
                    "bool" : "bool"
}


array_flip = {
                    "int" : "as-int",
                    "ric" : "as-ric",
                    "term-int" : "as-term-int",
                    "dis-int" : "as-dis-int", 
                    "term-dis-int" : "as-term-dis-int", 
                    "boxes" : "as-boxes",  
                    "zones" : "as-zones", 
                    "oct" : "as-oct", 
                    "pk" : "as-pk", 
                    "as-int" : "int", 
                    "as-ric" : "ric", 
                    "as-term-int" : "term-int", 
                    "as-dis-int" : "dis-int", 
                    "as-term-dis-int" : "term-dis-int", 
                    "as-boxes" : "boxes", 
                    "as-zones" : "zones", 
                    "as-oct" : "oct", 
                    "as-pk" : "pk", 
                    "bool" : "bool"
}