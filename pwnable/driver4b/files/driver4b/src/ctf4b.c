#include "ctf4b.h"
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/uaccess.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("pwnyaa");
MODULE_DESCRIPTION("SECCON Beginners CTF 2023 Online");

char g_message[CTF4B_MSG_SIZE] = "Welcome to SECCON Beginners CTF 2023!";

/**
 * Open this driver
 */
static int module_open(struct inode *inode, struct file *filp)
{
  return 0;
}

/**
 * Close this driver
 */
static int module_close(struct inode *inode, struct file *filp)
{
  return 0;
}

/**
 * Handle ioctl request
 */
static long module_ioctl(struct file *filp, unsigned int cmd, unsigned long arg)
{
  char *msg = (char*)arg;

  switch (cmd) {
    case CTF4B_IOCTL_STORE:
      /* Store message */
      memcpy(g_message, msg, CTF4B_MSG_SIZE);
      break;

    case CTF4B_IOCTL_LOAD:
      /* Load message */
      memcpy(msg, g_message, CTF4B_MSG_SIZE);
      break;

    default:
      return -EINVAL;
  }

  return 0;
}

static struct file_operations module_fops = {
  .owner = THIS_MODULE,
  .unlocked_ioctl = module_ioctl,
  .open = module_open,
  .release = module_close,
};

static dev_t dev_id;
static struct cdev c_dev;

static int __init module_initialize(void)
{
  if (alloc_chrdev_region(&dev_id, 0, 1, CTF4B_DEVICE_NAME))
    return -EBUSY;

  cdev_init(&c_dev, &module_fops);
  c_dev.owner = THIS_MODULE;

  if (cdev_add(&c_dev, dev_id, 1)) {
    unregister_chrdev_region(dev_id, 1);
    return -EBUSY;
  }

  return 0;
}

static void __exit module_cleanup(void)
{
  cdev_del(&c_dev);
  unregister_chrdev_region(dev_id, 1);
}

module_init(module_initialize);
module_exit(module_cleanup);
