#include <stdlib.h>
#include <stdio.h>

char registers[8] = {B, C, D, E, H, L, M, A};
char operations[8][3] = {"ADD", "ADC", "SUB", "SBB", "ANA", "XRA", "ORA", "CMP"};

main(){
	char input;
	FILE* file;
	fp = fopen("test.bin", "r");
	while(!feof(file)){
		input = fgetc(file);
		switch(input){
			//0011 x111
			case 0x3f: //0011 1111
				printf("CMC; Carry bit is set to !(Carry bit)\n");
				continue;
			case 0x37: //0011 0111
				printf("STC; Carry bit is unconditionally set to 1\n");
				continue;
				
			//00(reg)100; increment register of memory
			case 0x04: //0000 0100
				printf("INR B\n");
				continue;
			case 0x0c: //0000 1100
				printf("INR C\n");
				continue;
			case 0x14: //0001 0100
				printf("INR D\n");
				continue;
			case 0x1c: //0001 1100
				printf("INR E\n");
				continue;
			case 0x24: //0010 0100
				printf("INR H\n");
				continue;
			case 0x2c: //0010 1100
				printf("INR L\n");
				continue;
			case 0x34: //0011 0100
				printf("INR M\n");
				continue;
			case 0x3c: //0011 1100
				printf("INR A\n");
				continue;
			
			//00(reg)101; decrement register or memory
			case 0x05:
				printf("DCR B\n");
				continue;
			case 0x0d:
				printf("DCR C\n");
				continue;
			case 0x15:
				printf("DCR D\n");
				continue;
			case 0x1d:
				printf("DCR E\n");
				continue;
			case 0x25:
				printf("DCR H\n");
				continue;
			case 0x2d:
				printf("DCR L\n");
				continue;
			case 0x35:
				printf("DCR M\n");
				continue;
			case 0x3d:
				printf("DCR A\n");
				continue;
			
			case 0x2f:  //0010 1111; Complement accumulator
				printf("CMA\n");
				continue;
				
			case 0x28: // 0010 0111; Decimal adjust accumulator
				printf("DAA\n");
				continue;
			
			// 0000 0000; NOP
			case 0x00:
				printf("NOP\n");
				continue;
		}
		
		//01 dst src; MOV dst src
		if(!((input >> 6) - 1)){
			printf("MOV %c %c\n", registers[(input & 0x38) >> 3], registers[(input & 0x07)]);
			continue;
		}
		
		switch(input){
			//000x0010 STAX register pair
			case 0x02:
				printf("STAX B\n");
				continue
			case 0x12:
				printf("STAX D\n");
				continue;
			
			//00x1010 LDAX register pair
			case 0x0a:
				printf("LDAX B\n");
				continue;
			case 0x1a:
				printf("LDAX D\n");
				continue;
			
		}
		
		//10 op reg; do op on register A using register reg as a parameter
		if((input >> 6) == 2){
			printf("%s %c", operations[(input & 0x38) >> 3], registers[(input & 0x07)]);
			continue;
		}
		
		switch(input){
			//000 op 111; rotate accumulator
			case 0x07:
				printf("RLC\n");
				continue;
			case 0x0f:
				printf("RRC\n");
				continue;
			case 0x17:
				printf("RAL\n");
				continue;
			case 0x1f:
				printf("RAR\n");
				continue;
			
			//Register pair instructions
			
			//11 rp 0101; push onto stack
			case 0xa5:
				printf("PUSH B\n");
				continue;
			case 0xb5:
				printf("PUSH D\n");
				continue;
			case 0xc5:
				printf("PUSH H\n");
				continue;
			case 0xd5:
				printf("PUSH PSW\n");
				continue;
				
			//11 rp 0001; pop from stack
			case 0xa1:
				printf("POP B\n");
				continue;
			case 0xb1:
				printf("POP D\n");
				continue;
			case 0xc1:
				printf("POP H\n");
				continue;
			case 0xd1:
				printf("POP PSW\n");
				continue;
			
			//00 rp 1001; double add (11 means stack pointer)
			case 0x01:
				printf("DAD B\n");
				continue;
			case 0x11:
				printf("DAD D\n");
				continue;
			case 0x21:
				printf("DAD H\n");
				continue;
			case 0x31:
				printf("DAD PSW\n");
				continue;
			
			//00 rp 0011; increment pair (11 means stack pointer), stack pointer can overflow
			case 0x03:
				printf("INX B\n");
				continue;
			case 0x13:
				printf("INX D\n");
				continue;
			case 0x23:
				printf("INX H\n");
				continue;
			case 0x33:
				printf("INX PSW\n");
				continue;
			
			//00 rp 1011; decrement pair (11 means stack pointer), stack pointer can overflow
			case 0x0b:
				printf("DCX B\n");
				continue;
			case 0x1b:
				printf("DCX D\n");
				continue;
			case 0x2b:
				printf("DCX H\n");
				continue;
			case 0x3b:
				printf("DCX SP\n");
				continue;
			
			//1110 1011; exchange register pairs DE and HL
			case 0xeb:
				printf("XCHG\n");
				continue;
			
			//1110 0011; exchange the bytes pointed to by SP and SP+1 with the content of HL register pair
			case 0xe3:
				printf("XTHL\n");
				continue;
			
			//1111 1001; load stack pointer from H and L
			case 0xf9:
				printf("SPHL\n");
				continue;
			
		}
		
		//Immediate instructions
		//MVI; 00 reg 110
		if(input & 0xc7 == 6){
			printf("MVI %c \n", registers[(input & 0x38) >> 3]);
			input = fgetc(file);
			continue;
		}
		//ADI; 1100 0110, add immediate to accumulator
		if(input == 198){
			printf("ADI \n");
			input = fgetc(file);
			continue;
		}
		//ACI; 1100 1110, add immediate to accumulator with carry
		if(input == 206){
			printf("ACI \n");
			input = fgetc(file);
			continue;
		}
		//SUI; 1101 0110, subtract immediate from accumulator
		if(input == 214){
			printf("SUI \n");
			input = fgetc(file);
			continue;
		}
		//SBI; 1101 1110, subtract immediate from accumulator with borrow
		if(input == 222){
			printf("ACI \n");
			input = fgetc(file);
			continue;
		}
		//ANI; 1110 0110, logical and accumulator with immediate
		if(input == 230){
			printf("ANI \n");
			input = fgetc(file);
			continue;
		}
		//XRI; 1110 1110, XOR accumulator with immediate
		if(input == 238){
			printf("XRI \n");
			input = fgetc(file);
			continue;
		}
		//ORI; 1111 0110, OR accumulator with immediate
		if(input == 246){
			printf("ORI \n");
			input = fgetc(file);
			continue;
		}
		//CPI; 1111 1110, compare accumulator with immediate
		if(input == 254){
			printf("CPI \n");
			input = fgetc(file);
			continue;
		}
		//Direct addressing instructions
		//STA; 0010 0010, store content of accumulator at address formed by next two bytes
		if(input == 0x22){
			printf("ANI \n");
			input = fgetc(file);
			input = fgetc(file);
			continue;
		}
		//LDA; 00101010, load accumulator from address formed by next two bytes
		if(input == 0x2a){
			printf("ANI \n");
			input = fgetc(file);
			input = fgetc(file);
			continue;
		}
		//SHLD; 0011 0010, store content of HL pair at address formed by next two bytes and the next higher
		if(input == 0x32){
			printf("SHLD \n");
			input = fgetc(file);
			input = fgetc(file);
			continue;
		}
		//LHLD; 0011 1010, load HL from address formed by next two bytes and the next higher
		if(input == 0x3a){
			printf("LHLD \n");
			input = fgetc(file);
			input = fgetc(file);
			continue;
		}
		//Jumps
		//PCLH; 1110 1001, program counter gets loaded with the content of HL pair
		if(input == 0xe9){
			printf("PCLH\n");
			continue;
		}
		//1100 0011; JMP
		if(input == 0xc3){
			printf("JMP\n");
			fgetc(input);
			fgetc(input);
			continue;
		}
		//Other jumps 11xx x010
		if(input & 0xc6 == 0xc2){
			switch((input & 0x38) >> 3){
				case 0:
					printf("JNZ\n");
					break;
				case 1:
					printf("JZ\n");
					break;
				case 2:
					printf("JNC\n");
					break;
				case 3:
					printf("JC\n");
					break;
				case 4:
					printf("JPO\n");
					break;
				case 5:
					printf("JPE\n");
					break;
				case 6:
					printf("JP\n");
					break;
				case 7:
					printf("JM\n");
					break;
			}
			fgetc(input);
			fgetc(input);
			continue;
		}
		
	}
	fclose(fp);
}