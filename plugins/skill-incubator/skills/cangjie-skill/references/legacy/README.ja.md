# cangjie-skill

開発者向けに、アクセス可能な資料をプラグイン内の知識提案または paper ATOM CARD
へ蒸留します。

インストール可能な Skill や単なる要約は生成しません。AI が利用意図に基づいて
`type`、tags、書き込み動作を提案します。ユーザー確認後、paper カードは
`plugins/paper-project/knowledge/cards/atoms/` に保存できます。物理知識は提案のみとし、
計算候補を正式知識へ昇格しません。

開発時の書き込み前には、必ず `../prl-shared/SKILL.md` とプラグイン内 INDEX を読みます。
