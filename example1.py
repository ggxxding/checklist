import checklist
from checklist.test_suite import TestSuite

#导入测试套件
suite_path = 'release_data/sentiment/sentiment_suite.pkl'
suite = TestSuite.from_file(suite_path)

#导入模型预测结果
pred_path = 'release_data/sentiment/predictions/bert'
suite.run_from_file(pred_path, overwrite=True)

#分析预测结果
suite.summary() # or suite.visual_summary_table()