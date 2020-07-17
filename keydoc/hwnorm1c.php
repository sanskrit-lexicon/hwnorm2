<?php
// This is a php version of hwnorm1c.py.  (7/14/2020)
// It is written as an interactive function.
// The normalize_key function is self-contained and may be
// used elsewhere.
// function($b) {return preg_replace('//','',$b);};
function normalize_key($a) {
 $aM = function($b) {return preg_replace('/aM$/','a',$b);};
 $aH = function($b) {return preg_replace('/aH$/','a',$b);};
 $uH = function($b) {return preg_replace('/uH$/','u',$b);};
 $iH = function($b) {return preg_replace('/iH$/','i',$b);};
 $ttr_tr = function($b) {return preg_replace('/ttr/','tr',$b);};
 $ant_at = function($b) {return preg_replace('/ant$/','at',$b);};
 $normalize_key_C = function($b) {
  if (strpos($b,'C') == False) {return $b;}
  # X + C -> XcC  (X a vowel)
  $b1 = preg_replace('/([aAiIuUfFxXeEoO])C/','\1cC',$b);
  # X + cC -> XC  (X a consonant)
  $b2 = preg_replace('/([kKgGNcCjJYwWqQRtTdDnpPbBmyrlvhzSsHM])cC/','\1C',$b1);
  return $b2;
 };
 $rxx_rx = function($b) {return preg_replace('/([r])(.)\2/','\1\2',$b);};

$homorganic_nasal = function($b) {
  return preg_replace_callback('/(M)([kKgGNcCjJYwWqQRtTdDnpPbBm])/',
   function($matches) {
    #n = $matches[1] is  always M
    $c = $matches[2];
    $slp1_cmp1_helper_data = array(
    'k'=>'N','K'=>'N','g'=>'N','G'=>'N','N'=>'N',
    'c'=>'Y','C'=>'Y','j'=>'Y','J'=>'Y','Y'=>'Y',
    'w'=>'R','W'=>'R','q'=>'R','Q'=>'R','R'=>'R',
    't'=>'n','T'=>'n','d'=>'n','D'=>'n','n'=>'n',
    'p'=>'m','P'=>'m','b'=>'m','B'=>'m','m'=>'m'
    );
    $nasal = $slp1_cmp1_helper_data[$c];
    return ($nasal . $c);

   },
   $b);
};
/*
 $rxX_helper_data = array(
 'k'=>'K','g'=>'G',
 'c'=>'C','j'=>'J',
 'w'=>'W','q'=>'Q',
 't'=>'T','d'=>'D',
 'p'=>'P','b'=>'B'
 );

 $rxX_helper = function($matches) {
  $x = $matches[1];
  $X = $matches[2];
  if (array_key_exists($x,$rxX_helper_data) &&
      ($X == $rxX_helper_data[$x])) {
   return 'r' . $X; 
  } else {
   # no change
   return 'r' . $x . $X;
  }
 };
*/

 $rxX_rx = function($b) {

  return preg_replace_callback('/r(.)(.)/',
 
  function ($matches) { // anonymous function
  $x = $matches[1];
  $X = $matches[2];
 $rxX_helper_data = array(
 'k'=>'K','g'=>'G',
 'c'=>'C','j'=>'J',
 'w'=>'W','q'=>'Q',
 't'=>'T','d'=>'D',
 'p'=>'P','b'=>'B'
 );

  if (array_key_exists($x,$rxX_helper_data)) {
   if($X == $rxX_helper_data[$x]) {
    echo "rxX_rx: x=$x, X=$X\n";
    return 'r' . $X;
   }
  }
  # no change
  return 'r' . $x . $X;
 }
 ,
   $b);
 };
 $rules = array(
  array('Mm',$homorganic_nasal),
  array('aM',$aM),
  array('aH',$aH),
  array('uH',$uH),
  array('iH',$iH),
  array('ttr',$ttr_tr),
  array('ant',$ant_at),
  array('cC',$normalize_key_C),
  array('rxx',$rxx_rx),
  array('rxX',$rxX_rx)
 );
 foreach($rules as $rule) {
  list($code,$f) = $rule;
  $b = $f($a);
  if($b != $a) {echo "$code.  $a -> $b\n";}
  $a = $b;
 }
 return $a;
}
while (True) {
 $a = fgets(STDIN);
 $a = trim($a);
 if ($a == '') {break;}
 $ans = normalize_key($a);
 echo("$a -> $ans\n");
}

?>
