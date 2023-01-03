import sys
import os
import string
import time



class ModifiedLog():
	
	def __init__(self,FileName):
		
		self.FileName = FileName
		print (str(self.FileName))
		
	def WriteDebugLog(self, sMessage, sStatus=None):
		"""Public method to write Debug Level Message."""
		#print(sStatus)
		sTime  = time.strftime('%H:%M:%S')
		SDate  = time.strftime('%d-%m-%Y')
		sMode  = 'a'
		if sStatus is None:
			with open(self.FileName, sMode) as the_file:                
				the_file.writelines('{0:120} \n'.format(" [" + SDate + " " + sTime + "]    [DEBUG]        " + sMessage))                
				the_file.close()
		else:
			
			with open(self.FileName, sMode) as the_file:                
				the_file.writelines('{0:120} ==> {1:s}\n'.format(" [" + SDate + " " + sTime + "]    [DEBUG]        " + sMessage,sStatus))                
				the_file.close()

	# @INFO: Function to write Info Level Message.
	def WriteInfoLog(self, sMessage, sStatus=None):
		"""Public method to write Information Level Message."""
		sTime  = time.strftime('%H:%M:%S')
		SDate  = time.strftime('%d-%m-%Y')
		sMode  = 'a'
		if sStatus is None:
			with open(self.FileName, sMode) as the_file:                
				the_file.writelines('{0:120} \n'.format(" [" + SDate + " " + sTime + "]    [INFO ]        " + sMessage))                
				the_file.close()
		else:
			
			with open(self.FileName, sMode) as the_file:                
				the_file.writelines('{0:120} ==> {1:s}\n'.format(" [" + SDate + " " + sTime + "]    [INFO]        " + sMessage,sStatus))                
				the_file.close()


	# @INFO: Function to write Error Level Message.
	def WriteErrorLog(self, sMessage, sStatus=None):
		"""Public method to write Error Level Message."""
		sTime  = time.strftime('%H:%M:%S')
		SDate  = time.strftime('%d-%m-%Y')
		sMode  = 'a'
		if sStatus is None:
			with open(self.FileName, sMode) as the_file:                
				the_file.writelines('{0:120} \n'.format(" [" + SDate + " " + sTime + "]    [ERROR]        " + sMessage))                
				the_file.close()
		else:
			
			with open(self.FileName, sMode) as the_file:                
				the_file.writelines('{0:120} ==> {1:s}\n'.format(" [" + SDate + " " + sTime + "]    [ERROR]        " + sMessage,sStatus))                
				the_file.close()

	def WriteClientLog(self, sMessage, sStatus=None):
		"""Public method to write Error Level Message."""
		sMode  = 'a'
		if sStatus is None:
			with open(self.FileName, sMode) as the_file:                
				the_file.writelines(sMessage)            
				the_file.close()
		

	def WritePrint(self, sMessage, sStatus=None):
		sTime  = time.strftime('%H:%M:%S')
		SDate  = time.strftime('%d-%m-%Y')

		if (sStatus == None) and (("ERROR" in sMessage) or ("FAIL" in sMessage)):
			sStatus = "ERROR"


		if sMessage == "":
			pass

		elif (sStatus == None) or (str(sStatus).upper() == "INFO"):
			print("-> [INFO] " + str(sMessage))
			self.WriteInfoLog(sMessage)

		elif (str(sStatus).upper() == "DEBUG"):
			print("-> [DEBUG] " + str(sMessage))
			self.WriteDebugLog(sMessage)

		elif (str(sStatus).upper() == "ERROR"):
			print("-> [ERROR] " + str(sMessage))
			self.WriteErrorLog(sMessage)



	def WritePrintClient(self, sMessage, sStatus=None):
		self.WriteClientLog(sMessage)
		print(str(sMessage))

	   

		


if __name__ == '__main__':
	TestObj = ModifiedLog('C:\\TEST.log')
	TestObj.WriteDebugLog('A TEST DEBUG')
	TestObj.WriteInfoLog('A TEST INFO')
	TestObj.WriteErrorLog('A TEST ERROR')
	