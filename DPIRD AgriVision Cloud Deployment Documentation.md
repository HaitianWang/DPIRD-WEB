

# DPIRD AgriVision Cloud Deployment Documentation

This document provides a step-by-step guide to deploy DPIRD AgriVision on AWS using Lightsail and Route 53 for domain management.

------

## Step 1: Register an AWS Account

1. Go to the [AWS homepage](https://aws.amazon.com/).
2. Click **Sign Up** and follow the steps to create your account.
3. After registration, log in to your AWS Management Console.

------

## Step 2: Create a Lightsail Instance

1. Open the [AWS Lightsail Console](https://lightsail.aws.amazon.com/).
2. Click **Create instance**.
3. Select your instance location (choose a region close to your target users).
4. Choose **Linux/Unix** as the platform.
5. Choose the blueprint for your instance. Select **OS Only** and choose **Amazon Linux 2023** as the operating system.
6. For instance plan, select **Dual-stack** as the network type and select an instance size based on your requirements (2 GB RAM and 2 vCPUs would be enough for this project).
7. Name your instance (e.g., `agrivision-server`) and click **Create instance**.
8. Wait for the instance to initialize. Once it's ready, click on the instance to view its details.

------

## Step 3: Set Up a Domain Name with Lightsail DNS

### Option 1: Register a New Domain via AWS (Route 53)

If you don't have a domain yet, you can register one through AWS Route 53 and then use the Lightsail DNS zones to manage your domain. Follow the steps below.

#### Registering a Domain Using Route 53

1. Go to the [Route 53 Console](https://console.aws.amazon.com/route53/).

2. In the Route 53 dashboard, click **Registered domains** on the left menu.

3. Click the **Register domain** button.

4. In the **Search for a new domain name** section, type your desired domain name and click **Search** to see if it's available.

5. Select an available domain and click **Select**.

6. Click **Proceed to checkout** to proceed with the domain registration.

7. Fill in your contact details as required by the domain registrar (this includes name, address, and email).

8. Review the information and complete the registration by clicking **Submit**.

   > **Note**: Domain registration may take a few minutes to process. AWS will notify you by email when the registration is complete.

------

### Option 2: Use an Existing Domain

If you already own a domain through another provider (such as GoDaddy, Namecheap, etc.), you can skip the domain registration part.

------

## Step 4: Set Up a Lightsail DNS Zone and Assign Name Servers

### 1. Create a DNS Zone in Lightsail

1. Go to the [AWS Lightsail Console](https://lightsail.aws.amazon.com/).
2. In the Lightsail dashboard, click **Domain & DNS** from the top menu.
3. Click **Create DNS zone**.
4. Enter your domain name and click **Create DNS zone**.

### 2. Assign Lightsail's Name Servers to Your Domain

Once the DNS zone is created, Lightsail will provide you with a list of name servers.

1. Copy the **Name Servers** provided by Lightsail (you will see them listed after creating the DNS zone).

2. Go to your domain registrar (where you purchased your domain, e.g., Route 53, GoDaddy or Namecheap).

3. In your domain management dashboard, look for an option to update **Name Servers**.

4. Replace your current name servers with the ones provided by Lightsail. This will route all DNS queries for your domain through AWS Lightsail.

   > **Note**: DNS changes can take a few minutes to a few hours to propagate.

### 3. Create DNS Records in Lightsail

Now, you will configure your domain to point to your Lightsail instance.

1. In your Lightsail DNS zone, click on **DNS records** and **Add record**.
2. Create an `A` record to map your domain (or subdomain) to your Lightsail instance's IP:
   - **Record type**: Choose `A` (IPv4 address).
   - **Record name**: Leave this blank to use the root domain (e.g., `example.com`), or enter `www` if you want to create a subdomain like `www.example.com`.
   - **Resolves to**: Enter the **Static IP** of your Lightsail instance (you can find this on the Lightsail instance dashboard).
3. Click **Save**.

## Step 5: Access the Lightsail Instance

1. From the Lightsail dashboard, click on your instance.

2. Click **Connect using SSH**.


------

## Step 6: Pull the DPIRD AgriVision Code from the Repository

1. Install Git if it’s not already installed:

   ```bash
   sudo dnf update -y
   sudo dnf install git -y
   ```

2. Clone the DPIRD AgriVision repository:

   ```bash
   git clone https://github.com/HaitianWang/DPIRD-WEB.git
   ```
   
3. Navigate to the repository folder:

   ```bash
   cd DPIRD-WEB
   ```

------

## Step 7: Modify Code for Deployment

Now, update any necessary configuration files and any required environment variables in the repository (e.g., server's actual IP address, API keys).

### 1. Backend

Navigate to the `back-end` folder.

1. **Modify `app.py`**

- In `app.py`, change:

  ```python
  app.run(host='127.0.0.1', port=5003, debug=True)
  ```

  to:

  ```python
  app.run(host='0.0.0.0', port=5003, debug=True)
  ```

2. **Set OpenAI API Key**

- In `routes/file_operations.py`, update the OpenAI key:

  ```python
  openai.api_key = "your_openai_api_key"
  ```

### 2. Frontend

Navigate to the `front-end` folder.

1. **Update `server_url` in Frontend Components**

- In the following files inside `src/components`, update `server_url` from `http://127.0.0.1:5003` with the actual server IP:
  - `frontPage.vue`
  - `regiPage.vue`
  - `uploadPage.vue`
  - `userPage.vue`

  ```vue
  server_url: "http://<your-server-IP>:5003"
  ```

2. **Update `package.json` Scripts**

- In `package.json`, ensure the `dev` and `serve` scripts are configured correctly:

  ```json
  "dev": "webpack-dev-server --disableHostCheck=true --inline --progress --config build/webpack.dev.conf.js"
	```
	```json
  "serve": "http-server dist -p 80"
  ```

3. **Modify `config/index.js`**

- In `config/index.js`, set the application to run on port 80 and listen on all interfaces:

  ```js
  host: '0.0.0.0',
  port: 80
  ```


------

## Step 8: Run the Program

### 1. Backend

Navigate to the `back-end` folder.

1. **Install `pip` and Create Virtual Environment**

   ```bash
   sudo dnf install python3-pip -y
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Backend Application**

   ```bash
   nohup python3 app.py > app.log 2>&1 &
   ```

### 2. Frontend

Navigate to the `front-end` folder.

1. **Install Dependencies**

   ```bash
   npm install
   ```

2. **Run Frontend in a Screen Session**

   ```bash
   screen -S myapp
   nohup sudo npm run dev > app.log 2>&1 &
   ```

------

## Step 9: Access the Application

Open a web browser and visit your domain or the public IP address of your Lightsail instance. You should see the login page of DPIRD AgriVision.

