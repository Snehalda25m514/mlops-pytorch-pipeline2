1)	STEP - 1
First make a local folder structure by running below python code -
 
Where, Make_repo.py ->
import os
# Define the exact folder mapping required
structure = [
    "mlops-pytorch-pipeline2/.github/workflows/ci.yml",
    "mlops-pytorch-pipeline2/configs/training_config.yaml",
    "mlops-pytorch-pipeline2/docker/Dockerfile.train",
    "mlops-pytorch-pipeline2/docker/Dockerfile.serve",
    "mlops-pytorch-pipeline2/k8s/namespace.yaml",
    "mlops-pytorch-pipeline2/k8s/training-job.yaml",
    "mlops-pytorch-pipeline2/k8s/serving-deployment.yaml",
    "mlops-pytorch-pipeline2/k8s/serving-service.yaml",
    "mlops-pytorch-pipeline2/k8s/configmap.yaml",
    "mlops-pytorch-pipeline2/k8s/hpa.yaml",
    "mlops-pytorch-pipeline2/requirements/train.txt",
    "mlops-pytorch-pipeline2/requirements/serve.txt",
    "mlops-pytorch-pipeline2/src/train.py",
    "mlops-pytorch-pipeline2/src/model.py",
    "mlops-pytorch-pipeline2/src/dataset.py",
    "mlops-pytorch-pipeline2/src/serve.py",
    "mlops-pytorch-pipeline2/tests/test_model.py",
    "mlops-pytorch-pipeline2/README.md",
    "mlops-pytorch-pipeline2/.gitignore"
]
print("Initializing directory structures...")
for path in structure:
    # Safely isolate the file name to resolve target folders
    directory = os.path.dirname(path)
    
    # Generate folders recursively if they don't exist yet
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    # Instantiate blank structural templates
    if not os.path.exists(path):
        with open(path, 'w') as f:
            pass            
print("Initialization successful! All folders and files generated.")
2)	STEP - 2

Now go to git ->
https://github.com/Snehalda25m514?tab=repositories

	Create “New” repository manually without doing any selection (empty repository) 

3)	STEP -3 
Run cmd
On command line, once you are in respective directory(newly created), run below commands -  
E:\MTech\Term3\MLOps\Assignment3\mlops-pytorch-pipeline2>git remote set-url origin https://github.com/Snehalda25m514/mlops-pytorch-pipeline2
E:\MTech\Term3\MLOps\Assignment3\mlops-pytorch-pipeline2>git branch -M main
E:\MTech\Term3\MLOps\Assignment3\mlops-pytorch-pipeline2>git push -u origin main
 
------------------------------------ End – Git main repository created --------------------------------------------------- 










---------------------------------------- PR #1 Start – Creating develop branch from main -------------------------
4)	STEP 4 
	Create “develop” branch
 
Create feature pipeline –
 
5)	STEP 5
	Now make changes to your files (source code and configurations)
 
6)	STEP 6 – 
	Check if code pipeline works locally -

pip install -r .\requirements\train.txt
 

python src/train.py
 
 



	Test serve.py locally
 

pip install -r .\requirements\serve.txt


 
	Start server
$env:PYTHONPATH = "src" 
uvicorn src.serve:app --host 0.0.0.0 --port 8080

 

 
	Open another Powershell window, check health – 
Invoke-RestMethod -Uri http://localhost:8080/health 


 

Finally test > 
curl.exe -X POST -F "file=@sample.jpg" http://localhost:8080/predict
 



7)	STEP 7
	 Stage the files changed
git add src/ configs/ requirements/
git commit -m "feat: implement baseline network layers, dataset loaders, and training logic"
git push -u origin feature/core-pipeline
 


8)	STEP 8
	Open and Merge PR #1 on GitHub:
•	Go to your repository webpage on GitHub.
•	Click Compare & pull request.
•	Change the base branch dropdown from main to develop.
•	Title it: feat: add core training pipeline scripts
•	Type a clear description outlining the code added to the src/ directory.
•	Click Create pull request, then click Merge pull request

 






--------------------------- #PR 2 Second Feature Branch (feature/docker-training) ----------

9)	STEP 9
	pull the merged code from PR #1
git checkout develop 
git pull origin develop
git checkout -b feature/docker-training

	Update the files
o	 docker/Dockerfile.train 
o	docker/Dockerfile.serve
Note: Before committing the changes to the git, the changes done for docker-training need to be tested. As I do not have docker installed locally I am testing at IITM server - 164.52.205.84 
	Login to server with credentials given – 
ssh <username>@164.52.205.84
   	       Enter Password
	Copy the working folder to IITM server
 

	Test the updated code –
Test 1: Verify the Training Dockerfile Compiles
Run below command at IITM server, in that folder  
docker build -t mlops-train:test -f docker/Dockerfile.train .

 
	

Test 2
	Run the training container
docker run --rm -v "%cd%/outputs:/app/outputs" mlops-train:test 

or 

mkdir -p outputs 
docker run --rm \ -v "$(pwd)/outputs:/app/outputs" \ mlops-train:test

 
 

 
 

	Test 3 - Verify Training Artifact Exists 
 ls -la outputs/
	 

Test 4: Verify the Serving Dockerfile Compiles
docker build -t mlops-serve:test -f docker/Dockerfile.serve .
 
	Test 5: Run the Serving Dockerfile 
docker run -d \ -p 8080:8080 \ -v "$(pwd)/outputs:/app/outputs" \ --name isolated-api \ mlops-serve:test sleep 5
		test the health –
curl -i http://localhost:8080/health
 

		prediction –
At one terminal -
source venv/bin/activate
export PYTHONPATH=src 
uvicorn src.serve:app --host 0.0.0.0 --port 8080

And at another terminal -
python3 -c "from PIL import Image; Image.new('RGB', (32, 32), color='blue').save('test_sample.jpg')"
curl -X POST -F "file=@test_sample.jpg" http://localhost:8080/predict
OR 
On same terminal with pillow installation-
 

10)	STEP 10
	Complete the PR in git
•	Go to your repository webpage on GitHub.
•	Click Compare & pull request.
•	Change the base branch dropdown from main to develop.
•	Title it: feat: add core training pipeline scripts
•	Type a clear description outlining the code added to the src/ directory.
•	Click Create pull request, then click Merge pull request

 

	Complete the merge in git 

•	Go to your repository webpage on GitHub.
•	Click Compare & pull request.
•	Change the base branch dropdown from main to develop.
•	Title it: feat: add core training pipeline scripts
•	Type a clear description outlining the code added to the src/ directory.
•	Click Create pull request, then click Merge pull request

  

 









--------------------------------- PR #3 – Kubernetes – orchestration --------------------------------------
	STEP 11 – 
o	Change the files inside the k8s/ folder –
namespace.yaml, configmap.yaml, training-job.yaml, serving-deployment.yaml,
serving-service.yaml and hpa.yaml

o	Validate on IITM server if changes are correct – run command on IITM server once the updated folder is available there. 
python3 -c "import yaml, glob; [list(yaml.safe_load_all(open(f))) for f in glob.glob('k8s/*.yaml')]; print('Validation Passed: All Kubernetes manifests contain perfect multi-document YAML structural syntax')"
 
		
Do the git push and merge

 
 


----------------------------------- PR #4 Continuous Integration (CI) automation workflows ------------------
STEP 12 – Make changes to workflows/ci.yml and test in GitActions and merge
	Pull the latest code 
 

	Modify 
                    .github/workflows/ci.yml

	Push and merge in git

git add .github/workflows/ci.yml
git commit -m "ci: configure linting rules and structural schema checks for kubernetes manifests"
git push origin feature/ci-automation
 

1.	Open your internet browser and navigate to your GitHub repository dashboard.
2.	Click the green Compare & pull request activation banner.
3.	Verify that your target base branch dropdown selector matches develop.
4.	Title it exactly following your standards: ci: implement workflow automation pipelines
5.	Click Create pull request.

 
 



	Test changes
Navigate to the Actions tab on your repository to watch your new CI job run and turn green.

 


6.	Once it passes successfully, go back to the PR page and click Merge pull request.
 


 



STEP 13: Merge everything into your production main branch to finish:
git checkout main 
git pull origin main 
git merge develop --no-ff -m "chore: release week 1 and week 2 verified milestones to production" 
git push origin main
 


The graphical view –
git log –oneline –graph --all
  
 

 








What is the most challenging part?
The most challenging aspect of this assignment lay in orchestrating a complex, multi-stage machine learning lifecycle within a tightly constrained, non-root cloud server infrastructure running Rootless Docker. While designing a Convolutional Neural Network (CNN) for CIFAR-10 classification and writing FastAPI inference endpoints required careful implementation, the real engineering friction emerged when shifting those scripts into production-ready containers and local Kubernetes clusters under intense host-level environment restrictions.
Rootless Docker isolates user namespaces to enhance security, but it places extreme limitations on system-level network routing and disk storage capabilities. The primary hurdle manifested as a persistent No space left on device error during the container compilation phase. Because deep learning frameworks like PyTorch and Torchvision require several gigabytes of extraction space, Rootless Docker quickly exhausted the server’s tiny default home partition cache.
Overcoming this required moving beyond standard configurations. Traditional workarounds—such as altering global system daemons via /etc/docker/daemon.json or invoking administrative commands—were completely blocked because the profile lacked sudo privileges. Attempts to bypass this by shifting project directories or redirecting standard build targets using the DOCKER_TMPDIR environment variable were consistently overridden by the underlying containerd runtime cache engines.
The ultimate solution required an advanced architectural pivot: decoupling local storage limitations from workflow validation by orchestrating a space-optimized Continuous Integration (CI) loop inside GitHub Actions. To ensure the multi-gigabyte images could still be validated sequentially without hitting system storage limits, I implemented a strict build-run-prune pipeline sequence inside the GitHub runner. The training image was compiled and executed first to generate the model weights file. Once that artifact was securely harvested, an aggressive docker system prune -a -f was triggered to completely wipe the host cache before compiling the serving image.
This infrastructure challenge was further compounded during the final Kubernetes deployment phase using Minikube. The rootless network isolation layers caused silent, lingering port-forwarding collisions, resulting in a recurrent bind: address already in use error that prevented the local cluster from initializing. Resolving this required debugging the low-level RootlessKit PortManager to identify how internal bridges map random routing tables. Ultimately, explicitly configuring an isolated proxy layer using arbitrary port masks forced Minikube to bypass the network blocks entirely.
This assignment proved that true MLOps engineering is not just about writing accurate model code. The greatest challenge—and the most valuable learning experience—was successfully debugging hidden infrastructure layers, managing tight hardware constraints, and engineering creative automation workarounds to deploy a functional pipeline under strict security constraints.


