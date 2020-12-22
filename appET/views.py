from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
import json
from wit import Wit
from timefhuman import timefhuman
import spacy
access_token = '************************'


class Datetimeissue(APIView):
    def get(self, request, *args, **kwargs):
        data = {"Name": request.query_params.get("Name","")}
        json_string1 = json.dumps(data)
        
        # line split the input & make ready for timefhuman
        field_x = json_string1.split('"')[3]
        
        # this line for replace next to upcoming for week days error resolution
        field = field_x.replace("next","upcoming")
        print(field)

        # main code "timefhuman" this pass the time
        list_all =[]
        try:
            qwe = timefhuman(field)
            json_string2 = json.dumps(qwe, sort_keys=True, default=str)
            print(json_string2)

        
        
            # check total number of timeset
            x = json_string2.split(',')
            num = len(x)
            print(num)
        
            count = 0
            # if midnight word in the input so pass 00:00:00
            
            while(count < num):
                asd = json_string2.split(',')[count]
                print(asd)
                yy = str(asd).split('"')[1]
                print(yy)
                date = str(yy).split(' ')[0]
                time = str(yy).split(' ')[1]
                year = str(yy).split('-')[0]
                month = str(yy).split('-')[1]
                day = date.split('-')[2]
                count = count+1
                list_all.extend([{"attribute":"Time", "value":time},
                    {"attribute":"Day", "value":day},
                    {"attribute":"Month", "value":month},
                    {"attribute":"Year", "value":year}])
                print(list_all)

        except:
            time = "Still Learning" 
            day = "Still Learning" 
            month = "Still Learning"
            year = "Still Learning"
            list_all.extend([{"attribute":"Time", "value":time},
                {"attribute":"Day", "value":day},
                {"attribute":"Month", "value":month},
                {"attribute":"Year", "value":year}])

        new_data = {
            "entries":[{
                "template_type":"set_attr",
                "attributes": list_all
            }]
        }        
        return JsonResponse(new_data, status=201)



class SpacyView(APIView):
    def get(self, request, *args, **kwargs):
        data = request.query_params.get("Name","")

        nlp = spacy.load("en_core_web_sm")
        doc = nlp(data)

        print(doc)

        list_all = []

        for ent in doc.ents:
            print(ent.label_, ent.text)
            list_all.append({"attribute":"DATE", "value":ent.text})
        
        if not list_all:
            #print("asb 123 1 1232412#$ %^&*")
            list_all.append({"attribute":"DATE", "value":"empty string"})
        
        print(list_all)

        new_data = {
            "entries":[{
                "template_type":"set_attr",
                "attributes": list_all
            }]
        } 

        return JsonResponse(new_data, status=201)


class Wiitaii(APIView):
    def get(self, request, *args, **kwargs):
        data = request.query_params.get("Name","")
        print(data)

        access_token = '*************************'

        client = Wit(access_token)
        qwe = client.message(data)
        print(qwe)
        json_string1 = json.dumps(qwe)

        field_x = json_string1.split('entities')[1]
        print("skjbwejbc ibeb erh !@#$%^&*%^ #$%^&")
        print(field_x)

        list_all = []
        list_all.append({"attribute":"DATE", "value":"empty string"})
        print(list_all)

        new_data = {
            "entries":[{
                "template_type":"set_attr",
                "attributes": list_all
            }]
        } 

        return JsonResponse(new_data, status=201)

