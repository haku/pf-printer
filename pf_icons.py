from udchar import Udchars

ACTIONS_FREE = Udchars("free", 9, 24,
    #0         0         0         0    5
    "                                    "  #  0
    "                                    "  #  1
    "                                    "  #  2
    "                                    "  #  3
    "                                    "  #  4
    "                                    "  #  5
    "                                    "  #  6
    "                                    "  #  7
    "       xx                           "  #  8
    "      xxxx                          "  #  9
    "     xx  xx                         "  # 10
    "    xx    xx                        "  # 11
    "   xxx     xx                       "  # 12
    "  xxxxx     xx                      "  # 13
    " xx  xxx     xx                     "  # 14
    "xx    xxx     xx                    "  # 15
    "xx    xxx     xx                    "  # 16
    " xx  xxx     xx                     "  # 17
    "  xxxxx     xx                      "  # 18
    "   xxx     xx                       "  # 19
    "    xx    xx                        "  # 20
    "     xx  xx                         "  # 21
    "      xxxx                          "  # 22
    "       xx                           "  # 23
    )
ACTIONS_1 = Udchars("   *", 9, 24,
    #0         0         0         0    5
    "                                    "  #  0
    "                                    "  #  1
    "                                    "  #  2
    "                                    "  #  3
    "                                    "  #  4
    "                                    "  #  5
    "                                    "  #  6
    "                                    "  #  7
    "       xx                           "  #  8
    "      xxxx                          "  #  9
    "     xxxxxx                         "  # 10
    "    xxxxxxxx                        "  # 11
    "   xxxxxxxxxx                       "  # 12
    "    xxxxxxxxxx                      "  # 13
    " xx  xxxxxxxxxx                     "  # 14
    "xxxx  xxxxxxxxxx                    "  # 15
    "xxxx  xxxxxxxxxx                    "  # 16
    " xx  xxxxxxxxxx                     "  # 17
    "    xxxxxxxxxx                      "  # 18
    "   xxxxxxxxxx                       "  # 19
    "    xxxxxxxx                        "  # 20
    "     xxxxxx                         "  # 21
    "      xxxx                          "  # 22
    "       xx                           "  # 23
    )
ACTIONS_2 = Udchars("  **", 9, 24,
    #0         0         0         0    5
    "                                    "  #  0
    "                                    "  #  1
    "                                    "  #  2
    "                                    "  #  3
    "                                    "  #  4
    "                                    "  #  5
    "                                    "  #  6
    "                                    "  #  7
    "       xx                           "  #  8
    "      xxxx        xx                "  #  9
    "     xxxxxx      xxxx               "  # 10
    "    xxxxxxxx    xxxxxx              "  # 11
    "   xxxxxxxxxx  xxxxxxxx             "  # 12
    "    xxxxxxxxxx  xxxxxxxx            "  # 13
    " xx  xxxxxxxxxx  xxxxxxxx           "  # 14
    "xxxx  xxxxxxxxxx  xxxxxxxx          "  # 15
    "xxxx  xxxxxxxxxx  xxxxxxxx          "  # 16
    " xx  xxxxxxxxxx  xxxxxxxx           "  # 17
    "    xxxxxxxxxx  xxxxxxxx            "  # 18
    "   xxxxxxxxxx  xxxxxxxx             "  # 19
    "    xxxxxxxx    xxxxxx              "  # 20
    "     xxxxxx      xxxx               "  # 21
    "      xxxx        xx                "  # 22
    "       xx                           "  # 23
    )
ACTIONS_3 = Udchars(" ***", 9, 24,
    #0         0         0         0    5
    "                                    "  #  0
    "                                    "  #  1
    "                                    "  #  2
    "                                    "  #  3
    "                                    "  #  4
    "                                    "  #  5
    "                                    "  #  6
    "                                    "  #  7
    "       xx                           "  #  8
    "      xxxx        xx                "  #  9
    "     xxxxxx      xxxx        xx     "  # 10
    "    xxxxxxxx    xxxxxx      xxxx    "  # 11
    "   xxxxxxxxxx  xxxxxxxx    xxxxxx   "  # 12
    "    xxxxxxxxxx  xxxxxxxx  xxxxxxxx  "  # 13
    " xx  xxxxxxxxxx  xxxxxxxx  xxxxxxxx "  # 14
    "xxxx  xxxxxxxxxx  xxxxxxxx  xxxxxxxx"  # 15
    "xxxx  xxxxxxxxxx  xxxxxxxx  xxxxxxxx"  # 16
    " xx  xxxxxxxxxx  xxxxxxxx  xxxxxxxx "  # 17
    "    xxxxxxxxxx  xxxxxxxx  xxxxxxxx  "  # 18
    "   xxxxxxxxxx  xxxxxxxx    xxxxxx   "  # 19
    "    xxxxxxxx    xxxxxx      xxxx    "  # 20
    "     xxxxxx      xxxx        xx     "  # 21
    "      xxxx        xx                "  # 22
    "       xx                           "  # 23
    )
ACTIONS_123 = Udchars("  */**/***", 9, 24,
    #0         0         0         0         0         0         0         0         0        9
    "                                                                                          "  #  0
    "                                                                                          "  #  1
    "                                                                                          "  #  2
    "                                                                                          "  #  3
    "                                                                                          "  #  4
    "                                                                                          "  #  5
    "                                                                                          "  #  6
    "                                                                                          "  #  7
    "       xx                   xx                             xx                             "  #  8
    "      xxxx                 xxxx        xx                 xxxx        xx                  "  #  9
    "     xxxxxx               xxxxxx      xxxx               xxxxxx      xxxx        xx       "  # 10
    "    xxxxxxxx             xxxxxxxx    xxxxxx             xxxxxxxx    xxxxxx      xxxx      "  # 11
    "   xxxxxxxxxx           xxxxxxxxxx  xxxxxxxx           xxxxxxxxxx  xxxxxxxx    xxxxxx     "  # 12
    "    xxxxxxxxxx           xxxxxxxxxx  xxxxxxxx           xxxxxxxxxx  xxxxxxxx  xxxxxxxx    "  # 13
    " xx  xxxxxxxxxx       xx  xxxxxxxxxx  xxxxxxxx       xx  xxxxxxxxxx  xxxxxxxx  xxxxxxxx   "  # 14
    "xxxx  xxxxxxxxxx     xxxx  xxxxxxxxxx  xxxxxxxx     xxxx  xxxxxxxxxx  xxxxxxxx  xxxxxxxx  "  # 15
    "xxxx  xxxxxxxxxx     xxxx  xxxxxxxxxx  xxxxxxxx     xxxx  xxxxxxxxxx  xxxxxxxx  xxxxxxxx  "  # 16
    " xx  xxxxxxxxxx       xx  xxxxxxxxxx  xxxxxxxx       xx  xxxxxxxxxx  xxxxxxxx  xxxxxxxx   "  # 17
    "    xxxxxxxxxx           xxxxxxxxxx  xxxxxxxx           xxxxxxxxxx  xxxxxxxx  xxxxxxxx    "  # 18
    "   xxxxxxxxxx           xxxxxxxxxx  xxxxxxxx           xxxxxxxxxx  xxxxxxxx    xxxxxx     "  # 19
    "    xxxxxxxx             xxxxxxxx    xxxxxx             xxxxxxxx    xxxxxx      xxxx      "  # 20
    "     xxxxxx               xxxxxx      xxxx               xxxxxx      xxxx        xx       "  # 21
    "      xxxx                 xxxx        xx                 xxxx        xx                  "  # 22
    "       xx                   xx                             xx                             "  # 23
    )
ACTIONS_REACTION = Udchars("  <-", 9, 24,
    #0         0         0         0    5
    "                                    "  #  0
    "                                    "  #  1
    "                                    "  #  2
    "                                    "  #  3
    "                                    "  #  4
    "                                    "  #  5
    "                                    "  #  6
    "         xxxxxxxxxx                 "  #  7
    "      xxxxxxxxxxxxxxxx              "  #  8
    "    xxxxxx    xxxxxxxxxx            "  #  9
    "   xxxx          xxxxxxxx           "  # 10
    "  xxx              xxxxxxx          "  # 11
    " xx                 xxxxxx          "  # 12
    "x                    xxxxxx         "  # 13
    "                      xxxxx         "  # 14
    "                      xxxxx         "  # 15
    "                      xxxxx         "  # 16
    "          xxxxx      xxxxx          "  # 17
    "        xxxxxx     xxxxxxx          "  # 18
    "      xxxxxxxxxxxxxxxxxx            "  # 19
    "     xxxxxxxxxxxxxxxxx              "  # 20
    "      xxxxxxxxxxxxx                 "  # 21
    "        xxxxxx                      "  # 22
    "          xxxxx                     "  # 23
    )
ACTIONS_REACTION_BIG = Udchars("  <-", 9, 24,
    #0         0         0         0    5
    "         xxxxxxxxxxx                "  #  0
    "      xxxxxxxxxxxxxxxxx             "  #  1
    "    xxxxxxxxxxxxxxxxxxxxx           "  #  2
    "   xxxxxx    xxxxxxxxxxxxx          "  #  3
    "  xxxx           xxxxxxxxxx         "  #  4
    " xx                xxxxxxxxx        "  #  5
    "x                   xxxxxxxxx       "  #  6
    "                     xxxxxxxx       "  #  7
    "                      xxxxxxxx      "  #  8
    "                      xxxxxxxx      "  #  9
    "                       xxxxxxx      "  # 10
    "                       xxxxxxx      "  # 11
    "                       xxxxxxx      "  # 12
    "                       xxxxxx       "  # 13
    "                      xxxxxxx       "  # 14
    "            xxxxx     xxxxxx        "  # 15
    "          xxxxxx     xxxxxx         "  # 16
    "        xxxxxxx    xxxxxxx          "  # 17
    "      xxxxxxxxxxxxxxxxxx            "  # 18
    "     xxxxxxxxxxxxxxxxx              "  # 19
    "      xxxxxxxxxxxxxx                "  # 20
    "        xxxxxxx                     "  # 21
    "          xxxxxx                    "  # 22
    "            xxxxx                   "  # 23
    )
