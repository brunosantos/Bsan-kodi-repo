import re
import sys


class JsUnpacker:

    def unpackAll(self, data):
        sPattern = '(eval\(function\(p,a,c,k,e,d\)\{while.*?)\s*</script>'
        return re.sub(sPattern, lambda match: self.unpack(match.group(1)), data)

    def containsPacked(self, data):
        return 'p,a,c,k,e,d' in data

    def unpack(self, sJavascript):
        aSplit = sJavascript.split(";',")
        p = str(aSplit[0])
        aSplit = aSplit[1].split(",")
        a = int(aSplit[0])
        c = int(aSplit[1])
        k = aSplit[2].split(".")[0].replace("'", '').split('|')
        e = ''
        d = ''
        sUnpacked = str(self.__unpack(p, a, c, k, e, d))
        return sUnpacked.replace('\\', '')

    def __unpack(self, p, a, c, k, e, d):
        while (c > 1):
            c = c -1
            if (k[c]):
                p = re.sub('\\b' + str(self.__itoa(c, a)) +'\\b', k[c], p)
        return p

    def __itoa(self, num, radix):
        result = ""
        while num > 0:
            result = "0123456789abcdefghijklmnopqrstuvwxyz"[num % radix] + result
            num /= radix
        return result


class JsUnpackerV2:

    def unpackAll(self, data):
        try:
            in_data=data
            sPattern = '(eval\\(function\\(p,a,c,k,e,d.*)'
            enc_data=re.compile(sPattern).findall(in_data)
            #print 'enc_data',enc_data, len(enc_data)
            if len(enc_data)==0:
                sPattern = '(eval\\(function\\(p,a,c,k,e,r.*)'
                enc_data=re.compile(sPattern).findall(in_data)
                #print 'enc_data packer...',enc_data

            for enc_val in enc_data:
                unpack_val=self.unpack(enc_val)
                in_data=in_data.replace(enc_val,unpack_val)
            return in_data
        except:
            traceback.print_exc(file=sys.stdout)
            return data


    def containsPacked(self, data):
        return 'p,a,c,k,e,d' in data or 'p,a,c,k,e,r' in data

    def unpack(self,sJavascript,iteration=1, totaliterations=1  ):

        aSplit = sJavascript.split("rn p}('")

        p1,a1,c1,k1=('','0','0','')
        ss="p1,a1,c1,k1=(\'"+aSplit[1].split(".spli")[0]+')'
        exec(ss)

        k1=k1.split('|')
        aSplit = aSplit[1].split("))'")
        e = ''
        d = ''#32823
        sUnpacked1 = str(self.__unpack(p1, a1, c1, k1, e, d,iteration))
        if iteration>=totaliterations:
            return sUnpacked1
        else:
            return self.unpack(sUnpacked1,iteration+1)

    def __unpack(self,p, a, c, k, e, d, iteration,v=1):
        while (c >= 1):
            c = c -1
            if (k[c]):
                aa=str(self.__itoaNew(c, a))
                p=re.sub('\\b' + aa +'\\b', k[c], p)# THIS IS Bloody slow!
        return p

    def __itoa(self,num, radix):

        result = ""
        if num==0: return '0'
        while num > 0:
            result = "0123456789abcdefghijklmnopqrstuvwxyz"[num % radix] + result
            num /= radix
        return result

    def __itoaNew(self,cc, a):
        aa="" if cc < a else self.__itoaNew(int(cc / a),a)
        cc = (cc % a)
        bb=chr(cc + 29) if cc> 35 else str(self.__itoa(cc,36))
        return aa+bb