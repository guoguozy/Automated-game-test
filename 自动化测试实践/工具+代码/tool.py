def run_cmd(cmd):
    """执行CMD命令"""
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    return [i.decode() for i in p.communicate()[0].splitlines()]


def get_apk_info():
    """获取apk的package，activity名称

    :return: list  eg ['com.android.calendar', 'com.meizu.flyme.calendar.AllInOneActivity']
    """
    result = run_cmd("adb shell dumpsys activity top")
    for line in result:
        if line.strip().startswith('ACTIVITY'):
            return line.split()[1].split('/')

print(get_apk_info())

output: ['com.android.calendar', 'com.meizu.flyme.calendar.AllInOneActivity']


def get_mem_using(package_name=None):
    """查看apk的内存占用

    :param package_name:
    :return: 单位KB
    """
    if not package_name:
        package_name = get_apk_info()[0]
    result = run_cmd("adb shell dumpsys meminfo {}".format(package_name))
    info = re.search('TOTAL\W+\d+', str(result)).group()
    mem = ''
    try:
        mem = info.split()
    except Exception as e:
        print(info)
        print(e)
    return mem[-1]

output: 37769


def backup_current_apk(path=r"C:\Users\jianbing\Desktop\apks"):
    package = get_apk_info()[0]
    result = run_cmd("adb shell pm path {}".format(package))
    cmd = "adb pull {} {}".format(result[0].split(":")[-1], os.path.join(path, "{}.apk".format(package)))
    print(cmd)
    run_cmd(cmd)
