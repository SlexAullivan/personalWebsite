# AWS Wordpress EC2 image

## Launching the Instance

- For this project we use an Amazon Linux 2 AMI with the x86 architecture.

    ![](/images/wordpress/Untitled.png)

- The free tier `t2.micro` machine should be sufficient for the needs of this website. If the site gains a lot of traffic then we may need to upgrade this later.

    ![](/images/wordpress/Untitled1.png)

- When creating your instance you will need to create a public and private ssh key. AWS allows you to easily download your private key. **Make sure to download your public key into a safe place**, as this is the **only** time that you will be able to download this key. The name does not matter, just make sure you know where on your computer this key is located.

![](/images/wordpress/Untitled2.png)

## Connecting to your EC2 Instance

Change the permissions of your private key:

- Navigate to the directory where your private key is located and used the following command:
    - `chmod 400 <nameOfYourKey>.pem`

SSH into your ec2 instance

SSH stands for secure shell, this is a way to access a computer over the internet that you are not directly connected to. Using the terminal `cd` into the directory where your private key is located and use the following command:

- Go to the ec2 management console on AWS educate and find your instances public ipv4 address.
- In the terminal make sure you are in the folder where your `.pem` is located, the use the following command to ssh into your instance.
- `ssh -i <nameOfYourKey>.pem ec2-user@<public ipv4 address of your instance>`
- if prompted for ECDSA fingerprint, type `yes`

If you have done everything correctly you should be greeted by something that looks like the following:

![](/images/wordpress/Untitled3.png)

## Installing the LAMP stack

After successfully Connecting to the instance, we need to install the LAMP stack onto our ec2. Reconnect to your instance and follow the following instructions:

Note: The following commands are taken DIRECTLY from the AWS documentation [linked here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-lamp-amazon-linux-2.html).

1. Update Software packages: `sudo yum update -y`
2. Install the lamp-mariadb10.2-php7.2 and php7.2 Amazon Linux Extras repositories to get the latest versions of the LAMP MariaDB and PHP packages for Amazon Linux 2: 

    `sudo amazon-linux-extras install -y lamp-mariadb10.2-php7.2 php7.2`

3. Install Apache web server, MariaDB, and PHP packages:

    `sudo yum install -y httpd mariadb-server`

4. Start the Apache Web server:

    `sudo systemctl start httpd`

5. Configure the Apache Web server to Start when booted up:

    `sudo systemctl enable httpd`

    5.1. Verify `httpd` is on:

    `sudo systemctl is-enabled httpd`

    Should receive the following response: `enabled`

6.  Allow  inbound traffic by changing the inbound rules on your security group. [Official AWS documentation on changing security group rules here.](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/working-with-security-groups.html#adding-security-group-rule)
    - Under *Network & Security* on the left navigation bar. Click Security groups.

        ![](/images/wordpress/Untitled4.png)

    - Identify which security group to edit. For me it was Launch-wizard-1 that was already attached to my ec2 instance.

        ![](/images/wordpress/Untitled5.png)

    - using the CIDR block 0.0.0.0/0 allows all traffic to reach your web server, use this only for testing for a short while. Production environments should not use this rule.
7. Test the Web-server by visiting the  public DNS address. Find this on your instances management console.

    Because there is nothing in the `/var/www/html` folder we should get the apache test page

    ![](/images/wordpress/Untitled6.png)

### Setting File Permissions

Apache serves files  that are located in the Apache document root or `/var/www/html` which is owned be root by default. We need to give the `ec2-user` account permissions in order to manipulate files with the Apache Document root. Use the Following steps. [Again these steps are take directly from the AWS documentation linked here.](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-lamp-amazon-linux-2.html)

1. Add Your user to the Apache Group:

    `sudo usermod -a -G apache ec2-user`

2.  Logout and login again to make sure the `ec2-user` is part of the apache group.
    1. Logout with:

        `exit`

    2.  Reconnect to the instance via ssh, like before. Once connected check your groups with the following:

        `groups`

        You should see `apache` as one of the groups.

        ![](/images/wordpress/Untitled7.png)

3. Change the group ownership of `/var/www` and thus its contents to the Apache group:

    `sudo chown -R ec2-user:apache /var/www`

4. Add group write permissions and set the group ID on future subdirectories by changing the directory permissions of `/var/www` and its subdirectories:

    `sudo chmod 2775 /var/www && find /var/www -type d -exec sudo chmod 2775 {} \;`

5. add group write permissions by recursively changing the file permissions:

    `find /var/www -type f -exec sudo chmod 0664 {} \;`

### Testing the LAMP server

1. Create a PHP file in the Apache Document root:

    `echo "<?php phpinfo(); ?>" > /var/www/html/phpinfo.php`

2. View the PHP file we just created in the browser:

    [](http://my.public.dns.amazonaws.com/phpinfo.php)

    Make sure to use your instances public dns when viewing this page, you should get the following:

    ![](/images/wordpress/Untitled8.png)

3. Because this page gives information about specific software being used on your stack, we should not have it viewable over the internet for security reasons. Delete the PHP file:

    `rm /var/www/html/phpinfo.php`

### Secure the Database Server

MariaDB installs with features that are useful while developing however, they should not be used while in production. The following steps are how to secure the database; again these steps are taken directly from the AWS documentation linked before.

1. Start MariaDB server:

    `sudo systemctl start mariadb`

2. run `msql_secure_installation`

    `sudo mysql_secure_installation`

    You will be prompted to enter a root password. The by default there is no root password so press enter.

    Then you will be prompted to create a root password. Enter the Password, then press `y` for all of the options following.

3. To turn off the database (optional):

`sudo systemctl stop mariadb`

4. To start the database on boot-up (optional):

`sudo systemctl enable mariadb`

## Saving Your Instance as an Image

On the AWS ec2 management console select the instance that you have intalled the LAMP stack on.

- press Actions

![](/images/wordpress/Untitled9.png)

- Press Image and templates:
- Press Create image

![](/images/wordpress/Untitled10.png)

- You can find the Image that you created in the left nav bar under Images > AMIs

![](/images/wordpress/Untitled11.png)

Once the image has been created you can use that image to launch an instance with the LAMP stack already enabled from the AMIs page. Launch a second image and use that as a starting point to install wordpress.

## Installing WordPress

Connect to your new instance that already has the LAMP stack created and running on it. and follow the following instructions to install wordpress on your instance. These Instructions are taken directly from the AWS documentation found here.

1. Download the latest WordPress release with `wget`

    `wget [https://wordpress.org/latest.tar.gz](https://wordpress.org/latest.tar.gz)`

2. Unzip the installation package:

    `tar -xzf latest.tar.gz`

### Create Database user and databse for Wordpress

1. Start databse server:

    `sudo systemctl start mariadb`

2. Log in to databse server as `root` user, you should have made this passsword in an earlier step when configuring the lamp stack.

    `mysql -u root -p`

    - This will bring up the database interaction that looks like the following:

        `MariaDB [(none)]>`

    - Create a username and password with the following command:

        `CREATE USER 'wordpress-user'@'localhost' IDENTIFIED BY 'your_strong_password';`

        - Replace `wordpress-user` with a username
        - Replace `your_strong_password` with a password, avoid the `'` character or else you will break the command
3. Create the database, use a descriptive name like `wordpress-db`

    `CREATE DATABASE `wordpress-db`;`

4. Grant full privileges to the user created at step 2:

    `GRANT ALL PRIVILEGES ON `wordpress-db`.* TO "wordpress-user"@"localhost";`

    - make sure to change `wordpress-user` to the username you set earlier
5. Pick up all the changes you made by flushing the database:

    `FLUSH PRIVILEGES;`

6. Exit the mysql client:

    `exit`

### Create and Edit the wp-config.php file

1. Copy the sample config file to a file called `wp-config.php`

    `cp wordpress/wp-config-sample.php wordpress/wp-config.php`

2. Use Nano to edit the `wp-config.php` file. DO NOT USE VIM, unless you have used it before and know how to navigate using vim. find and edit the following lines, when editing make sure to use the values you set earlier.

    `nano wordpress/wp-config.php`

    1. Edit the line that defines the database name: `define('DB_NAME', 'wordpress-db');`
    2. Edit the line that defines the databse user: `define('DB_USER', 'wordpress-user');`
    3. Edit the line that defines the password: `define('DB_PASSWORD', 'your_strong_password');`
    4.  Go to this [link](https://api.wordpress.org/secret-key/1.1/salt/) and generate unique keys and salt.

    ```
    define('AUTH_KEY',         ' #U$$+[RXN8:b^-L 0(WU_+ c+WFkI~c]o]-bHw+)/Aj[wTwSiZ<Qb[mghEXcRh-');
    define('SECURE_AUTH_KEY',  'Zsz._P=l/|y.Lq)XjlkwS1y5NJ76E6EJ.AV0pCKZZB,*~*r ?6OP$eJT@;+(ndLg');
    define('LOGGED_IN_KEY',    'ju}qwre3V*+8f_zOWf?{LlGsQ]Ye@2Jh^,8x>)Y |;(^[Iw]Pi+LG#A4R?7N`YB3');
    define('NONCE_KEY',        'P(g62HeZxEes|LnI^i=H,[XwK9I&[2s|:?0N}VJM%?;v2v]v+;+^9eXUahg@::Cj');
    define('AUTH_SALT',        'C$DpB4Hj[JK:?{ql`sRVa:{:7yShy(9A@5wg+`JJVb1fk%_-Bx*M4(qc[Qg%JT!h');
    define('SECURE_AUTH_SALT', 'd!uRu#}+q#{f$Z?Z9uFPG.${+S{n~1M&%@~gL>U>NV<zpD-@2-Es7Q1O-bp28EKv');
    define('LOGGED_IN_SALT',   ';j{00P*owZf)kVD+FVLn-~ >.|Y%Ug4#I^*LVd9QeZ^&XmK|e(76miC+&W&+^0P/');
    define('NONCE_SALT',       '-97r*V/cgxLmp?Zy4zUU4r99QQ_rGs2LTd%P;|_e1tS)8_B/,.6[=UK<J_y9?JWG');
    ```

    Exit the file and save  by pressing: `ctrl+x`, `y`, then `enter`

### Install your WordPress files under the Apache Document Root

To have WordPress run at the document root do the following;

`cp -r wordpress/* /var/www/html`

### Allow WordPress to Use Permalinks

1. open `https.conf` file with nano:

    `sudo nano /etc/httpd/conf/httpd.conf`

2.  find the section that starts with: `<Directory "/var/www/html">`
3. inside this section there should be a line that says: `AllowOverride None`

    change the all to `All`

4. Exit nano the same way as above.

### Install the PHP graphics drawing library on Amazon Linux 2

1. Install  `php-gd`

    `sudo yum install php-gd`

2. Verify the install version, the following command `sudo yum list installed | grep php-gd` should give the following ouput `php72-gd.x86_64  7.2.30-1.22.amzn1  amzn-updates`

### Fix File Permissions for the Apache Web Server

Because WordPress needs to write to the Apache Document Root we need to change some permissions.

1. Grant file ownership of `/var/www`  to the apache user

    `sudo chown -R apache /var/www`

2. Grant ownership of `/var/www` to the apache group

    `sudo chgrp -R apache /var/www`

3. Change directory permissions of `/var/www` to add group write permissions and to set the group ID on future subdirectories:

    `sudo chmod 2775 /var/www
    find /var/www -type d -exec sudo chmod 2775 {} \;`

4. Change the file permissions of `/var/www` to add group write permissions:

    `find /var/www -type f -exec sudo chmod 0664 {} \;`

5. Restart the Apache Web server:

    `sudo systemctl restart httpd`

### Running the WordPress Installation Script

We are now ready to install wordpress.

1. use `systemctl` to ensure `https` and databse services start at boot up

    `sudo systemctl enable httpd && sudo systemctl enable mariadb`

2. Verify database is running:

    `sudo systemctl status mariadb` if not running use `sudo systemctl start mariadb` to start it.

3. verify Apache web server is running:

    `sudo systemctl status httpd` if not running use `sudo systemctl start httpd` to start it.

4. visit your public dns, you should see your word press website. Once youve gotten to this point, it would be wise to stop your instance and create an image from this instance.