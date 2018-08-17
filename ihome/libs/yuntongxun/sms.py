from .CCPRestSDK import REST


#主帐号
accountSid= '8aaf0708654176180165421b0eab0022';

#主帐号Token
accountToken= '12b58f4e0dab44bbbfd73cd52fa4ae11';

#应用Id
appId='8aaf0708654176180165421b0f0c0029';

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com';

#请求端口 
serverPort='8883';

#REST版本号
softVersion='2013-12-26';

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id

class CCP:
    """自己封装的发送短信的辅助类"""
    tag = None

    def __new__(cls):
        if cls.tag is None:
            
            cls.tag =  super().__new__(cls)
            cls.tag.rest = REST(serverIP,serverPort,softVersion)
            cls.tag.rest.setAccount(accountSid,accountToken)
            cls.tag.rest.setAppId(appId)
        
        return cls.tag

    def send_template_sms(self,to,datas,temp_id):

        result = self.rest.sendTemplateSMS(to,datas,temp_id)
        # for k,v in result.items():
        #     if k=='templateSMS' :
        #             for k,s in v.items(): 
        #                 print ("%s:%s"%(k, s))
        #     else:
        #         print ("%s:%s"%(k, v))
        status_code = result.get('statusCode')
        if status_code == "000000":
            #表示发送成功
            return 0
        else:
            return -1


    #初始化REST SDK
    
#sendTemplateSMS(手机号码,内容数据,模板Id)
if __name__ == "__main__":
    cpp = CCP()
    #id是魔板
    cpp.send_template_sms("13249700923",["hello_world","10"],1)

