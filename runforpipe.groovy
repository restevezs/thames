pipeline {
	agent any
      	stages{
		
        stage('Update branch') {
            steps {
                sh """#!/bin/bash
            			git merge develop --no-edit
            			git log --oneline -n 5
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
				 }
	  
	post {
	    
	
		success {
		    
        	
			mail (	to: "restevez@a2etechnologies.com",
                subject: "Errors contained in logs files",
                body: """Errors contained in logs files.
                
                details: ${env.BUILD_URL}
                    
                """)
                
                
                    
                
					
		}
		failure {
		    
			
			mail (	to: "restevez@a2etechnologies.com",
                subject: "Failed build ",
                body: """Errors contained in logs files.
                
                
                    
                """)
		
        			} 
		}
	  
      
	
	  
	
	   }
	   
