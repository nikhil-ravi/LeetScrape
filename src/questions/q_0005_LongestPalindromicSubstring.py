class Solution:
    """
    5. Longest Palindromic Substring
    
    Difficulty: Medium
    
    Given a string `s`, return the longest palindromic substring in `s`.
    
    Example 1:
    ```
    Input: s = "babad"
    Output: "aba"
    Explanation: "aba" is also a valid answer.
    ```
    Example 2:
    ```
    Input: s = "cbbd"
    Output: "bb"
    ```
    Example 3:
    ```
    Input: s = "aaaaa"
    Output: "aaaaa"
    ```
    Example 4:
    ```
    Input: s = "vmqjjfnxtyciixhceqyvibhdmivndvxyzzamcrtpywczjmvlodtqbpjayfchpisbiycczpgjdzezzprfyfwiujqbcubohvvyakxfmsyqkysbigwcslofikvurcbjxrccasvyflhwkzlrqowyijfxacvirmyuhtobbpadxvngydlyzudvnyrgnipnpztdyqledweguchivlwfctafeavejkqyxvfqsigjwodxoqeabnhfhuwzgqarehgmhgisqetrhuszoklbywqrtauvsinumhnrmfkbxffkijrbeefjmipocoeddjuemvqqjpzktxecolwzgpdseshzztnvljbntrbkealeemgkapikyleontpwmoltfwfnrtnxcwmvshepsahffekaemmeklzrpmjxjpwqhihkgvnqhysptomfeqsikvnyhnujcgokfddwsqjmqgsqwsggwhxyinfspgukkfowoxaxosmmogxephzhhy"
    Output: "oxaxo"
    ```
    Example 5:
    ```
    Input: s = "txzokgefxajgkrlhllbqmcrtbjpppdzugzketdvlaxametkejdfbcwxijjjywjzoedqduensgouechpbdthevggtdelqyejxvybvmttbkheqfyiartxmmuxbkixgslcmjondweiyuvztqntkmvkxqqlfxgotaexzejnmfrhvkgaxyxdxasxrjevzwfvwvmxqikvsfbhhznjsvrlzkwionopahxhcetbsacwrazeciknyczsrxpbblvskzfaimaoyxfcwcsfxlulcezkbiszclkcfawqefwbhalyqjtvedlwigklrkuzyfamqjgjmytxytrlwhttelgttxlizpypwccfhwhwtzyawxyjqnynfdgrqixbwfahrjvvoowehmhyllnfhnnaswfmjitjbftpyvbfgtywcvhcziempcmxlgfuktengaakiwbovlfdtkropqvntuawouofuebfqojpmbodeaaedobmpjoqfbeufouowautnvqporktdflvobwikaagnetkufglxmcpmeizchvcwytgfbvyptfbjtijmfwsannhfnllyhmhewoovvjrhafwbxiqrgdfnynqjyxwayztwhwhfccwpypzilxttgletthwlrtyxtymjgjqmafyzukrlkgiwldevtjqylahbwfeqwafcklczsibkzeclulxfscwcfxyoamiafzksvlbbpxrszcynkicezarwcasbtechxhaponoiwkzlrvsjnzhhbfsvkiqxmvwvfwzvejrxsaxdxyxagkvhrfmnjezxeatogxflqqxkvmktnqtzvuyiewdnojmclsgxikbxummxtraiyfqehkbttmvbyvxjeyqledtggvehtdbphceuogsneudqdeozjwyjjjixwcbfdjektemaxalvdtekzguzdpppjbtrcmqbllhlrkgjaxfegkozxt"
    Output: "txzokgefxajgkrlhllbqmcrtbjpppdzugzketdvlaxametkejdfbcwxijjjywjzoedqduensgouechpbdthevggtdelqyejxvybvmttbkheqfyiartxmmuxbkixgslcmjondweiyuvztqntkmvkxqqlfxgotaexzejnmfrhvkgaxyxdxasxrjevzwfvwvmxqikvsfbhhznjsvrlzkwionopahxhcetbsacwrazeciknyczsrxpbblvskzfaimaoyxfcwcsfxlulcezkbiszclkcfawqefwbhalyqjtvedlwigklrkuzyfamqjgjmytxytrlwhttelgttxlizpypwccfhwhwtzyawxyjqnynfdgrqixbwfahrjvvoowehmhyllnfhnnaswfmjitjbftpyvbfgtywcvhcziempcmxlgfuktengaakiwbovlfdtkropqvntuawouofuebfqojpmbodeaaedobmpjoqfbeufouowautnvqporktdflvobwikaagnetkufglxmcpmeizchvcwytgfbvyptfbjtijmfwsannhfnllyhmhewoovvjrhafwbxiqrgdfnynqjyxwayztwhwhfccwpypzilxttgletthwlrtyxtymjgjqmafyzukrlkgiwldevtjqylahbwfeqwafcklczsibkzeclulxfscwcfxyoamiafzksvlbbpxrszcynkicezarwcasbtechxhaponoiwkzlrvsjnzhhbfsvkiqxmvwvfwzvejrxsaxdxyxagkvhrfmnjezxeatogxflqqxkvmktnqtzvuyiewdnojmclsgxikbxummxtraiyfqehkbttmvbyvxjeyqledtggvehtdbphceuogsneudqdeozjwyjjjixwcbfdjektemaxalvdtekzguzdpppjbtrcmqbllhlrkgjaxfegkozxt"
    ```
    Example 6:
    ```
    Input: s = "ac"
    Output: "a"
    ```
    Example 7:
    ```
    Input: s = "wsgdzojcrxtfqcfkhhcuxxnbwtxzkkeunmpdsqfvgfjhusholnwrhmzexhfqppatkexuzdllrbaxygmovqwfvmmbvuuctcwxhrmepxmnxlxdkyzfsqypuroxdczuilbjypnirljxfgpuhhgusflhalorkcvqfknnkqyprxlwmakqszsdqnfovptsgbppvejvukbxaybccxzeqcjhmnexlaafmycwopxntuisxcitxdbarsicvwrvjmxsapmhbbnuivzhkgcrshokkioagwidhmfzjwwywastecjsolxmhfnmgommkoimiwlgwxxdsxhuwwjhpxxgmeuzhdzmuqhmhnfwwokgvwsznfcoxbferdonrexzanpymxtfojodcfydedlxmxeffhwjeegqnagoqlwwdctbqnuxngrgovrjesrkjrfjawknbrsfywljscfvnjhczhyeoyzrtbkvvfvofykkwoiclgxyaddhpdoztdhcbauaagjmfzkkdqexkczfsztckdlujgqzjyuittnudpldjvsbwbzcsazjpxrwfafievenvuetzcxynnmskoytgznvqdlkhaowjtetveahpjguiowkiuvikwewmgxhgfjuzkgrkqhmxxavbriftadtogmhlatczusxkktcsyrnwjbeshifzbykqibghmmvecwwtwdcscikyzyiqlgwzycptlxiwfaigyhrlgtjocvajcnqyenxrnjgogeqtvkxllxpuoxargzgcsfwavwbnktchwjebvwwhfghqkcjhuhuqwcdsixrkfjxuzvhjxlyoxswdlwfytgbtqbeimzzogzrlovcdpseoafuxfmrhdswwictsctawjanvoafvzqanvhaohgndbsxlzuymvfflyswnkvpsvqezekeidadatsymbvgwobdrixisknqpehddjrsntkqpsfxictqbnedjmsveurvrtvpvzbengdijkfcogpcrvwyf"
    Output: "xllx"
    ```
    
    Constraints:

    - `1 <= s.length <= 1000`
    - `s` consist of only digits and English letters.    
    """
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        if s[::1] == s[::-1] or n < 2:
            return s
        ans = [[False for _ in range(n)] for _ in range(n)]
        for i in range(n):
            ans[i][i] = True
        long_seq = s[0]
        for i in range(n, -1, -1):
            for j in range(i+1, n):
                if s[i] == s[j]:
                    ans[i][j]  = (j-i == 1 or ans[i+1][j-1])
                    if len(long_seq) < j-i+1 and ans[i][j]:
                        long_seq = s[i:j+1]
        return long_seq