from HTMLParser import HTMLParser

class sumParser(HTMLParser):
    #startTagDict={}
    #endTagDict={}
    #attrsDict={}
    #bagOfWords={}
    #script={}
    files=[];
    def handle_starttag(self, tag, attrs):
        if tag in self.files[len(self.files)-1][0]:
            self.files[len(self.files)-1][0][tag]+=1;
        else:
            self.files[len(self.files)-1][0][tag]=1;
        for a in attrs:
            if a in self.files[len(self.files)-1][1]:
                self.files[len(self.files)-1][1][tag]+=1;
            else:
                self.files[len(self.files)-1][1][tag]=1;
    def handle_endtag(self, tag):
        if tag in self.files[len(self.files)-1][2]:
            self.files[len(self.files)-1][2][tag]+=1;
        else:
            self.files[len(self.files)-1][2][tag]=1;
    def handle_data(self,data):
        currTag=self.get_starttag_text()
        if currTag != "script":
            words=data.split()
            for word in words:
                if word in self.files[len(self.files)-1][3]:
                    self.files[len(self.files)-1][3][word]+=1;
                else:
                    self.files[len(self.files)-1][3][word]=1;
        else:
            words=data.split()
            for word in words:
                if word in self.files[len(self.files)-1][4]:
                    self.files[len(self.files)-1][4][word]+=1;
                else:
                    self.files[len(self.files)-1][4][word]=1;
    def feed(self, data):
        props=[]
        for _ in range(0,5): props.append({})
        self.files.append(props);
        HTMLParser.feed(self, data)

    def resetParser(self):
        self.files=[]
        #print len(self.files)
    def __str__(self):
     return "Start Tags "+(str(self.startTagDict))+"\n"+"End Tags "+str(self.endTagDict)+"\n"+"Attributes "+str(self.attrsDict)+"\n"+"Bag of Words "+str(self.bagOfWords);
