pipeline {
	agent any
      	stages{
		
        stage('Update branch') {
            steps {
                sh """#!/bin/bash
            			
			git diff --name-only caliz..develop |& tee logfile_git_diff

		            """
                
            }
        }
      	    
            stage('Run synthesis') {
      	        steps {
      	            
      	            script{
      	                
      		            app_build=sh(script: """#!/bin/bash
      		            cd /Documents/runSynthesis/thames
      		
      	                python3 linter_status.py -r -l logfile_git_diff  
      	   
      		            """, returnStdout: true) as String
      	                    }
     
									}
									}
			stage('Run') {
      	        steps {
      	            echo "this is a test!"
     
									}
									}
				 }
	  

	  
      
	
	  
	
	   }
	   
