# mac_scripts
Mac 环境工作中可以用到的一些脚本

#### find_private_symbol.py
- 查找第三方模块中引用到的私有符号(non-public API)
- Usage: find_private_symbol.py /path/to/import/ privateSymbol

#### svn_add_exists_files.sh
- 手动添加文件到工程之后用此脚本快速添加到 svn 

#### svn_remove_deleted_files.sh
- 手动删除文件之后用此命令从 svn 删除

#### svn_revert_added_deleted_files.sh
- 添加了文件到 svn 但是又手动删除了文件之后用此命令 revert 掉 svn 的添加