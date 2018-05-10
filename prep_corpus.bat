 @echo off
 
 python "D:\kods\Step_3_replace_user_tag_link.py" "D:\korpusi\viksna2plus.tsv"

 python "D:\kods\Step_3_replace_Emoji.py" "D:\korpusi\viksna2plus_ustali.tsv"

 python "D:\kods\Step_3_replace_translit.py" "D:\korpusi\viksna2plus_ustali_emojis.tsv"

 python "D:\kods\Step_3_replace_num_punc.py" "D:\korpusi\viksna2plus_ustali_emojis_translit.tsv"

 python "D:\kods\Step_3_Stopwords.py" "D:\korpusi\viksna2plus_ustali_emojis_translit_num.tsv"

 python "D:\kods\Step_3_Stem.py" "D:\korpusi\viksna2plus_ustali_emojis_translit_num_stopwords.tsv"


 python "D:\kods\Step_3_replace_user_tag_link.py" "D:\korpusi\peisenieks.tsv"

 python "D:\kods\Step_3_replace_Emoji.py" "D:\korpusi\peisenieks_ustali.tsv"

 python "D:\kods\Step_3_replace_translit.py" "D:\korpusi\peisenieks_ustali_emojis.tsv"

 python "D:\kods\Step_3_replace_num_punc.py" "D:\korpusi\peisenieks_ustali_emojis_translit.tsv"

 python "D:\kods\Step_3_Stopwords.py" "D:\korpusi\peisenieks_ustali_emojis_translit_num.tsv"

 python "D:\kods\Step_3_Stem.py" "D:\korpusi\peisenieks_ustali_emojis_translit_num_stopwords.tsv"
