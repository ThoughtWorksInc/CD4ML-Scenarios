// https://nickcharlton.net/posts/setting-jenkins-credentials-with-groovy.html
import jenkins.model.Jenkins
import com.cloudbees.plugins.credentials.domains.Domain
import org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl
import com.cloudbees.plugins.credentials.CredentialsScope
import hudson.util.Secret

instance = Jenkins.instance
domain = Domain.global()
store = instance.getExtensionList(
  "com.cloudbees.plugins.credentials.SystemCredentialsProvider")[0].getStore()

def accessKey = System.getenv("ACCESS_KEY") ?: throw new Exception("NO ACCESS_KEY CONFIGURED")
def secretKey = System.getenv("SECRET_KEY") ?: throw new Exception("NO SECRET_KEY CONFIGURED")

secretAccessKey = new StringCredentialsImpl(
  CredentialsScope.GLOBAL,
  "ACCESS_KEY",
  "S3 Bucket Access Key",
  Secret.fromString(accessKey)
)
store.addCredentials(domain, accessKey)

secretAccessKey = new StringCredentialsImpl(
  CredentialsScope.GLOBAL,
  "SECRET_KEY",
  "S3 Bucket Secret Key",
  Secret.fromString(accessKey)
)
store.addCredentials(domain, secretKey)
