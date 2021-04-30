import checklist
from checklist.editor import Editor

import numpy as np
editor = Editor(language='chinese')
#checklist生成模板
ret = editor.template('{first_name}是一个来自{country}的{profession}。',
                       profession=['律师', '医生', '会计'])
print('==============checklist模板================')
print('{first_name}是一个来自{country}的{profession}.')
print('==============输出================')
print(np.random.choice(ret.data, 3))


ret = editor.template('今天的{mask}真{adj}。',  
                      adj=['不错', '棒','糟糕'])
print('==============语言模型建议================')
print('今天的{mask}真{adj}。  adj=[不错, 棒,糟糕]')
print('==============输出================')
print(np.random.choice(ret.data, 3))