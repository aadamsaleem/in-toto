import os
import sys
import subprocess
import argparse
from shutil import copyfile

NO_PROMPT = False

def prompt_key(prompt):
  if NO_PROMPT:
    print "\n" + prompt
    return
  inp = False
  while inp != "":
    try:
      inp = raw_input("\n%s -- press any key to continue" % prompt)
    except Exception, e:
      pass

def supply_chain():

  prompt_key("Define supply chain layout (Alice)")
  os.chdir("owner_alice")
  create_layout_cmd = "python create_layout.py"
  print create_layout_cmd
  subprocess.call(create_layout_cmd.split())

  prompt_key("Write code (Bob)")
  os.chdir("../functionary_bob")
  write_code_cmd = ("python -m toto.toto-run" +
                    " --step-name write-code --products foo.py" +
                    " --key bob -- vi foo.py")
  print write_code_cmd
  subprocess.call(write_code_cmd.split())
  copyfile("foo.py", "../functionary_carl/foo.py")


  prompt_key("Package (Carl)")
  os.chdir("../functionary_carl")
  package_cmd = ("python -m toto.toto-run" +
                 " --step-name package --material foo.py" +
                 " --products foo.tar.gz" +
                 " --key carl --record-byproducts" +
                 " -- tar zcvf foo.tar.gz foo.py")
  print package_cmd
  subprocess.call(package_cmd.split())


  prompt_key("Create final product")
  os.chdir("..")
  copyfile("owner_alice/root.layout", "final_product/root.layout")
  copyfile("functionary_bob/write-code.link", "final_product/write-code.link")
  copyfile("functionary_carl/package.link", "final_product/package.link")
  copyfile("functionary_carl/foo.tar.gz", "final_product/foo.tar.gz")


  prompt_key("Verify final product (client)")
  os.chdir("final_product")
  copyfile("../owner_alice/alice.pub", "alice.pub")
  verify_cmd = ("python -m toto.toto-verify" +
                " --layout root.layout" +
                " --layout-key alice.pub")
  print verify_cmd
  retval = subprocess.call(verify_cmd.split())
  print "Return value: " + str(retval)





  prompt_key("Tampering with the supply chain")
  os.chdir("../functionary_bob")
  tamper_cmd = "echo 'something evil' >> foo.py"
  print tamper_cmd
  subprocess.call(tamper_cmd, shell=True)
  copyfile("foo.py", "../functionary_carl/foo.py")


  prompt_key("Package (Carl)")
  os.chdir("../functionary_carl")
  package_cmd = ("python -m toto.toto-run" +
                 " --step-name package --material foo.py" +
                 " --products foo.tar.gz" +
                 " --key carl --record-byproducts" +
                 " -- tar zcvf foo.tar.gz foo.py")
  print package_cmd
  subprocess.call(package_cmd.split())


  prompt_key("Create final product")
  os.chdir("..")
  copyfile("owner_alice/root.layout", "final_product/root.layout")
  copyfile("functionary_bob/write-code.link", "final_product/write-code.link")
  copyfile("functionary_carl/package.link", "final_product/package.link")
  copyfile("functionary_carl/foo.tar.gz", "final_product/foo.tar.gz")


  prompt_key("Verify final product (client)")
  os.chdir("final_product")
  copyfile("../owner_alice/alice.pub", "alice.pub")
  verify_cmd = ("python -m toto.toto-verify" +
                " --layout root.layout" +
                " --layout-key alice.pub")
  print verify_cmd
  retval = subprocess.call(verify_cmd.split())
  print "Return value: " + str(retval)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-n", "--no-prompt", help="No prompt",
      action="store_true")
  args = parser.parse_args()
  if args.no_prompt:
    global NO_PROMPT
    NO_PROMPT = True

  supply_chain()

if __name__ == '__main__':
  main()
