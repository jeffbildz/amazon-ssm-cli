#!/usr/bin/python

import json
import os,sys,subprocess
import re,string,time
import boto,sys
from boto import ec2
from boto3.session import Session
from optparse import OptionParser


def ProcessCommand(server, command, region, profile):
  connection=ec2.connect_to_region(region)
  reservations=connection.get_all_instances();
 
  for reservation in reservations:
    for instances in reservation.instances:
      if sys.argv[1] in instances.tags['Name']:
         instance_id = instances.id 


  instance_ids = []
  instance_ids.append(instance_id)


  aws = Session(region_name=region, profile_name=profile)
  output = aws.client('ssm').send_command(
      InstanceIds=instance_ids,
      DocumentName='AWS-RunPowerShellScript',
      Parameters={
          "commands":[command],
          "executionTimeout":["3600"]
      }
  )
  command_id = output['Command']['CommandId']
  status = output['Command']['Status']
  print "Command: " + command_id + " Status: " + status
  time.sleep(5)

  output2 = aws.client('ssm').get_command_invocation(CommandId=command_id,InstanceId=instance_id)   
  status = output2['Status']

  while not status == "Success":
     time.sleep(5) 
     output2 = aws.client('ssm').get_command_invocation(CommandId=command_id,InstanceId=instance_id)  
     status = output2['Status']

  print output2['StandardOutputContent'] 


def main():
  #Loop through list of SQL servers
  server = sys.argv[1]
  command = sys.argv[2]
  region = sys.argv[3]
  profile = sys.argv[4]

  ProcessCommand(server, command, region, profile) 

if __name__ == '__main__':
    main()
