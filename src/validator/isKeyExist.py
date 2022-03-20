from typing import Dict, Any, Tuple

def isKeyExist(target: Dict[str, Any], keys: Tuple[str]) -> bool:
    """*argsに渡されたキー一覧が全てtargetに存在するのか確認する

    Args:
        target (Dict[str, Any]): 検索対象の辞書
        keys: (Tuple[str]): 検索したいキー一覧

    Returns:
        bool: 全て存在するならTrue, それ以外はFalse
    """
    for key in list(keys):
        if key not in target:
            return False
    
    return True