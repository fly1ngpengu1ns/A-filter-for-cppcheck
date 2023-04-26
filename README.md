# A-filter-for-cppcheck
 This is a script written in Python that can further filter out some unimportant information from cppcheck, which is more helpful for scanning large repositories.
## usage
1. 使用时, 需要将待检验的cppcheck检测结果存入同目录下的`output-cppcheck.txt`中,将代码保存在如`select.py`中, 使用`python3 select.py`即可在同目录下生成,  删除部分检测信息(error、warning和部分规则)的文件`AfterSelect.txt`, 和只含有warning,error和部分出错率高的信息的`WarnAndErr.txt`中.
2. 对于全局变量url_prefix的设置, 需要填入的是定位代码的网址前缀. 例如对于TencentOS-tiny仓库, 需要进入任意一个文件夹找到对应的前缀:https://github.com/OpenAtomFoundation/TencentOS-tiny/tree/master即可.
值得说明的是, 似乎/tree/master是文件夹的前缀, /blob/master是文件的前缀. 但无论是/tree/master或者是/blob/master都能进入文件中. 不过能否确定无论github还是gitee的仓库都是以/tree/master或者是/blob/master为前缀？如果是的话请联系我 修改下代码XD.
![url_prefix设置](https://github.com/fly1ngpengu1ns/A-filter-for-cppcheck/blob/main/photos/setting.png)
3. 对于全局变量dir_name的设置, 正如同注释所说的, 一般来说是git clone直接解压后, 使用cppcheck直接进行扫描的文件夹名称. 一般解压后, 仍以TencentOS-tiny为例, 是如同TencentOS-tiny-master这样的名称. 或者说, 在cppcheck的输出信息中, 开头的前缀即为dir_name的值. 因此需要注意的是, 请不要将此脚本直接运用于子文件夹扫描的结果, 如果存在这方面的需求可以手动修改url_prefix和dir_name的值！
4. 在设置正确后, 可以使用VsCode打开生成的WarnAndErr.txt文件, 可以直接跳转至url网页, 如果是github的仓库, 可以将github.com换成github.dev以打开在线IDE模式(启动速度稍微有点慢, 建议一眼看不出来的错再开起这个功能):
![效果展示](https://github.com/fly1ngpengu1ns/A-filter-for-cppcheck/blob/main/photos/result.png)
ps:此代码非常简陋, 欢迎各位在使用过程中进行补充修正！如果有发现肯定为fp的信息, 可以联系我添加至rules中!