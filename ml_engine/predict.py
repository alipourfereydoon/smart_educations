import json,sys
from .recommender import recommend
if __name__=='__main__':
 data=json.load(open(sys.argv[1],encoding='utf8')) if len(sys.argv)>1 else json.load(sys.stdin)
 print(json.dumps(recommend(data),ensure_ascii=False,indent=2))
