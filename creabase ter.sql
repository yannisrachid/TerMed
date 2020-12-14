SET SERVEROUTPUT ON ;
/* CREER TABLES*/
drop table connexion;
CREATE TABLE cheikh_connexion (
  adresse_mail varchar(30),
  mot_de_passe varchar(30) NOT NULL,
  numero_confirmation_mail number,
  compte_actif number NOT NULL,
  prenom varchar(30) NOT NULL,
  nom varchar(30) NOT NULL,
  data_naissance date,
  constraint pk_connexion primary key (adresse_mail),
  constraint ck_mdptaille check(length(mot_de_passe)>4)
);

/* PROCEDURE INSCRIPTION */

CREATE OR REPLACE PROCEDURE cheikh_inscription (vadresse_mail IN cheikh_connexion.adresse_mail%TYPE , vmot_de_passe IN cheikh_connexion.mot_de_passe%TYPE, 
vprenom IN cheikh_connexion.prenom%TYPE, vnom IN cheikh_connexion.nom%TYPE, vdata_naissance IN cheikh_connexion.data_naissance%TYPE, retour OUT NUMBER,
 num_confirmation out number) IS

BEGIN
num_confirmation:= DBMS_UTILITY.GET_TIME;
INSERT INTO cheikh_connexion values (vadresse_mail, vmot_de_passe, num_confirmation, 1, vprenom, vnom, vdata_naissance );
/* apres essayer d'envoyer par mail num conf pour mettre 0 et 1 apres*/
commit;
retour := 0;

EXCEPTION
WHEN DUP_VAL_ON_INDEX THEN
    DBMS_OUTPUT.PUT_LINE('Adresse mail déjà existant');
    retour := 1;
WHEN OTHERS THEN
    if (SQLERRM LIKE '%CK_MDPTAILLE%') THEN
    DBMS_OUTPUT.PUT_LINE('mot de passe trop court');
    retour:=2;
    else
    DBMS_OUTPUT.PUT_LINE(sqlerrm||' '||sqlcode);
    retour := 3;
    end if;
END;
/


/*INSERTION POUR TEST CONNEXION*/

/*Séquence pour les identifiants*/

INSERT INTO cheikh_connexion  VALUES
('berk', 'aaaaghjjkn', 1000, 1, 'bvnbvb', 'nnnnn', to_date('15-01-1997','DD-MM-YYYY'));

INSERT INTO cheikh_connexion  VALUES
('moi', 'aaaaghjjkn', 1000, 0, 'bvnbvb', 'nnnnn', to_date('15-01-1997','DD-MM-YYYY'));

commit;
declare
retour number;
conf number;
begin
cheikh_inscription('freezz', 'reuoojoi', 'jfjk', 'hjbsdkjcjk', '15-12-1225', retour, conf);
end;

select * from cheikh_connexion