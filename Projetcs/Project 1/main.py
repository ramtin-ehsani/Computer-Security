import Affine
import Vigenere


def main():
    ciphertext = "Lqrserpr Bmlthqq DuFftrur bes nrwr Nayjqbqu 11, 1974 nr Lav Frgqojw, Cmonjodqne, tth trlk fmmlp rk " \
                 "Mryhqmn PlHepdlt enp itvmqu hsmuf gsow dwxiew Liodjj HiOduvia. Knw fmwmir uv tj Ifdqmaz dsh Gquren " \
                 "phxgezw, frd tlx qofkjv, wtr nw Gquren-nrwr, ie rk Kedpfr azg Wyselfr azfjwtdb. Mms ylihlq qfqe, " \
                 "Ilqlexp, bes tlx qafhwrax jwenpifxhqu'x jidvy rayh. Qiozdwho'e ifxhqu med mfmmehhi qizrw wtmwzw ae " \
                 "ds erflxx azg imsfunfufrw sf oxqx capng barp xifojw, azg bes qyjr dqsngtqg nr sqyjvax lxwuqv tj " \
                 "Ayhwmcmq Xtlqqisr, fkj guxw ximu-dzxonltkrmsmmcmo hsmuf gsow vjviqv gc tth qetq 'Kfvvqb Uikmu', " \
                 "f jruhsh or Jjsrsh'x. Peaqfvda'v uirrrwqazfj wkuoqw bqffqe aeamogv ys huv uerqqyw emuqc oz, " \
                 "dsh arwjv sujsmns knq ub znxh m wfpezw fkezw blo idsxep Ojsnmuis ta sjvfaur ynphw xhq vyegq qfqe " \
                 "Xhsry Ilqpimpx, HiOduvia ejkaz dutemunrg aq f ruyejv or wjpehlxmoz ftqmquhmaxv frd qgzgafltrax " \
                 "swsgddrw. "
    # ciphertext = "Pjo mvvqzo aqnjob qi m pyno gv sgzgmlnjmtopqa iwtipqpwpqgz aqnjob kjobo omaj loppob qz mz " \
    #             "mlnjmtop qi smnnoh pg qpi zwsobqa ouwqdmlozp ozabynpoh wiqzc m iqsnlo smpjosmpqaml vwzapqgz mzh " \
    #             "agzdobpoh tmae pg m loppob.".upper()

    if Affine.main(ciphertext) is None:
        Vigenere.main(ciphertext)


if __name__ == '__main__':
    main()
